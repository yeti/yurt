from fabric.context_managers import prefix, settings
from fabric.operations import local, os
import re

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
    :return: String from text
    """
    with open(path, 'r') as file_item:
        result = file_item.read()
    return result


def recursive_file_modify(path, dictionary, pattern=r"%\(({})\)s"):
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
    for item in os.listdir(path):
        itempath = os.path.join(path, item)
        # If directory, call this function again
        if os.path.isdir(itempath) and not(itempath in [".", ".."]):
            recursive_file_modify(itempath, dictionary, pattern)
        else:
            # Get text, find all the variables, and then for each variable found,
            # create a new pattern and run re.sub to substitute all instances with
            # the dictionary
            file_text = get_file_text(itempath)
            change_vars = re.findall(all_vars_pattern, file_text)
            print "itempath: " + itempath,
            print "change_vars: " + str(change_vars)
            for variable in change_vars:
                var_pattern = pattern.format(variable)
                if "." in variable:
                    env_key, variable = variable.split('.')
                    target_dictionary = dictionary.get(env_key).copy()
                else:
                    target_dictionary = dictionary.copy()
                try:
                    file_text = re.sub(var_pattern, target_dictionary.get(variable), file_text)
                except TypeError:
                    import pdb
                    pdb.set_trace()
            with open(itempath, 'w') as change_file:
                change_file.write(file_text)


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
