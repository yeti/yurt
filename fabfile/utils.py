import json
import string
from Crypto.PublicKey import RSA
from fabric.context_managers import prefix, settings
from fabric.operations import local, os
import re
from random import choice
from fabric.state import env
import sys

__author__ = 'deanmercado'

###
# helper functions
###


def get_fab_settings():
    try:
        return __import__("fabric_settings", globals(), locals(), [], 0).FABRIC
    except ImportError:
        try:
            sys.path.append(".")
            return __import__("fabric_settings", globals(), locals(), [], 0).FABRIC
        except ImportError:
            raise ImportError('Create `fabric_settings.py` file in this directory')


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
    :param filepath: str
    :param dictionary: dict
    :param pattern: raw str
    :param all_vars_pattern: raw str
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


def recursive_file_modify(path, dictionary, pattern=r"%\(({0})\)s", is_dir=True):
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
    bash_path = '~/.bashrc'
    try:
        with open(os.path.expanduser(bash_path), 'r') as bashrc:
            bash_text = bashrc.read()
    except Exception:
        bash_path = '~/.bash_profile'
        with open(os.path.expanduser(bash_path), 'r') as bash_profile:
            bash_text = bash_profile.read()
    return bash_text, bash_path


def add_fab_path_to_bashrc():
    """
    Adds FAB_PATH variable to .bashrc
    :return: Void
    """
    with prefix('cd fabfile'):
        bashrc_text, bash_path = _get_bashrc()
        with open(os.path.expanduser(bash_path), 'w') as bashrc:
            if "export FAB_PATH" in bashrc_text:
                bashrc_text = re.sub(r'export FAB_PATH=[^\n]*\n', '', bashrc_text)
            bashrc.write(bashrc_text)
        local('echo "export FAB_PATH=$(pwd -P)" >> {0}'.format(bash_path))


def generate_printable_string(num_chars, special_chars=True):
    """
    Generates a random string of printable characters
    :param num_chars: number (int) of characters for the string to be
    :return: String
    """
    result = ""
    all_chars = string.printable.strip(string.whitespace)
    if not special_chars:
        all_chars = all_chars.strip(string.punctuation)
    while num_chars > 0:
        insert_char = choice(all_chars)
        if insert_char not in "\"'`\\{}$()":
            result = "".join((result, insert_char))
            num_chars -= 1
    return result


def generate_ssh_keypair(in_template=True):
    """
    Generates a 4096 bit ssh-keypair
    :param: bool
    :return: tuple (str, str)
    """
    key = RSA.generate(4096)
    public = key.publickey().exportKey('OpenSSH')
    if type(public) == ValueError:
        public = """
            This version of PyCrypto doesn't fully support key exporting to
            `OpenSSH` format. You can create a public key manually using `ssh-keygen`
            and the private key below. Replace this message with the public key
            (on one line).
        """
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
        Choose which environment (1-3) <{0}>:
        (1) Development
        (2) Staging
        (3) Production
         Choice:\t""").format(message)]
    except KeyError:
        environment = None
    return environment


def get_project_name_from_repo(repo_link, drop_hyphens=True):
    result = re.search(r"\.com[/:][^/]+/(.*)(\.git)?$", repo_link).group(1)
    result = re.sub(r"\.git$", "", result)
    if drop_hyphens:
        result = re.sub(r"\-", "", result)
    return result


def raw_input_wrapper(query, lower=False):
    usr_input = raw_input(query)
    if lower:
        usr_input = usr_input.lower()
    return usr_input


def pretty_print_dictionary(dictionary):
    print("{")
    for attr, value in dictionary.iteritems():
        print("{0} : {1}, ".format(attr, value))
    print("}\n")


def get_vault_credentials_from_path(path):
    vaults = []
    vault_keys = {}
    for path in os.listdir(path):
        vault_query = re.search(r"vault_([^\.]+)\.json", path)
        if vault_query:
            vaults.append(vault_query.group(0))
        for idx, vault in enumerate(vaults):
            vault_keys[str(idx)] = vault
    print("Option:\tVault:")
    for option_num, vault in vault_keys.iteritems():
        print("{0}:\t{1}".format(option_num, vault))
    vault_path = vault_keys[raw_input("Which vault do you want this server to access (use Option number)?:\t")]
    with open(vault_path, 'r') as vault_file:
        vault_details = json.loads(vault_file.read())
        return vault_details["VAULT_ADDR"], vault_details["VAULT_TOKEN"], vault_path
