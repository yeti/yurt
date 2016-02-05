import string
from Crypto.PublicKey import RSA
from fabric.context_managers import prefix, settings
from fabric.operations import local, os
import re
from random import choice
from fabric.state import env

__author__ = 'deanmercado'

###
# helper functions
###


def get_fab_settings():
    try:
        return __import__("fabric_settings", globals(), locals(), [], 0).FABRIC
    except Exception:
        raise Exception('Create `fabric_settings.py` file in this directory')


def get_file_text(path):
    """
    Gets the text from a file
    :param path:
    :return: String
    """
    with open(path, 'r') as file_item:
        result = file_item.read()
    return result


def _perform_substitution(filepath, dictionary, pattern, all_vars_pattern):
    """
    Get text, find all the variables, and then for each variable found,
    create a new pattern and run re.sub to substitute all instances with
    the dictionary
    :param filepath:
    :param dictionary:
    :param pattern:
    :param all_vars_pattern:
    :return: Void
    """
    file_text = get_file_text(filepath)
    change_vars = re.findall(all_vars_pattern, file_text)
    for variable in change_vars:
        var_pattern = pattern.format(variable)
        if "." in variable:
            env_key, variable = variable.split('.')
            target_dictionary = dictionary.get(env_key).copy()
        else:
            target_dictionary = dictionary.copy()
        file_text = re.sub(var_pattern, target_dictionary.get(variable), file_text)
    with open(filepath, 'w') as change_file:
        change_file.write(file_text)


def recursive_file_modify(path, dictionary, pattern=r"%\(({})\)s", is_dir=True):
    """
    Recursively modifies all files in a given directory with a replacement dictionary
    :param path: a given path
    :param dictionary: a dictionary of key-value pairs that must be replaced in files
    :param pattern: a regex-pattern that is searched for in each file (the default searches for "%()s")
    :return: Void
    """
    # Pattern for finding all the variables invoked in a file
    all_vars_pattern = pattern.format(r"[^\)]*")

    # Iterates through every item in the given path
    if is_dir:
        for item in os.listdir(path):
            itempath = os.path.join(path, item)
            # If directory, call this function again
            if os.path.isdir(itempath) and not(itempath in [".", ".."]):
                recursive_file_modify(itempath, dictionary, pattern)
            else:
                _perform_substitution(itempath, dictionary, pattern, all_vars_pattern)
    else:
        _perform_substitution(path, dictionary, pattern, all_vars_pattern)


def _get_bashrc():
    """
    Gets the text in ~/.bashrc
    :return: String, the bashrc text
    """
    with open(os.path.expanduser('~/.bashrc'), 'r') as bashrc:
        bashrc_text = bashrc.read()
    return bashrc_text


def install_virtualenvwrapper():
    """
    Installs virtualenvwrapper globally, adding to $HOME/.bashrc the required lines
    :return: Void
    """
    with settings(warn_only=True):
        local('pip install virtualenvwrapper')

    VIRTUALENV_EXPORT_LINES = [
        "export WORKON_HOME=$HOME/.virtualenvs",
        "export PROJECT_HOME=$HOME/Devel",
        "source /usr/local/bin/virtualenvwrapper.sh\n"
    ]

    bashrc_text = _get_bashrc()

    with open(os.path.expanduser('~/.bashrc'), 'w') as bashrc:
        for export_line in VIRTUALENV_EXPORT_LINES:
            if export_line not in bashrc_text:
                bashrc_text = "\n".join((bashrc_text, export_line))
        bashrc.write(bashrc_text)


def add_fab_path_to_bashrc():
    """
    Adds FAB_PATH variable to .bashrc
    :return: Void
    """
    with prefix('cd fabfile'):
        bashrc_text = _get_bashrc()
        with open(os.path.expanduser('~/.bashrc'), 'w') as bashrc:
            if "export FAB_PATH" in bashrc_text:
                bashrc_text = re.sub(r'export FAB_PATH=[^\n]*', '', bashrc_text)
            bashrc.write(bashrc_text)
        local('echo "export FAB_PATH=$(pwd -P)" >> ~/.bashrc')


def generate_printable_string(num_chars):
    """
    Generates a random string of printable characters
    :param num_chars: number (int) of characters for the string to be
    :return: String
    """
    result = ""
    all_chars = string.printable.strip(string.whitespace)
    while num_chars > 0:
        result = "".join((result, choice(all_chars)))
        num_chars -= 1
    result = re.sub(r"'", "\\'", result)
    return result


def generate_ssh_keypair(in_template=True):
    """
    Generates a 4096 bit ssh-keypair
    :return: Tuple (str, str)
    """
    key = RSA.generate(4096)
    public = key.publickey().exportKey('OpenSSH')
    private = key.exportKey('PEM')
    if in_template:
        private = re.sub(r"\n", "\n  ", private)
    return public, private


def get_environment_pem(message='', name_only=False):
    env.settings = get_fab_settings()
    if name_only:
        environments = {
            '1': 'development',
            '2': 'staging',
            '3': 'production'
        }
    else:
        environments = {
            '1': env.settings.get('development'),
            '2': env.settings.get('staging'),
            '3': env.settings.get('production')
        }
    try:
        environment = environments[raw_input("""
        Choose which environment (1-3) <{}>:
        (1) Development
        (2) Staging
        (3) Production
         Choice:\t""").format(message)]
    except KeyError:
        environment = None
    return environment
