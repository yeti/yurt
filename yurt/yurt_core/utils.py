import json
import string
import hvac
from Crypto.PublicKey import RSA
import re
from random import choice
from requests import ConnectionError
import os

__author__ = 'deanmercado'

###
# helper functions
###


def add_settings(vault, git_repo, test_mode=False):
    """
    Return a settings dict that can be used to generate a new project
    :param vault: boolean, do we have a vault that can be looked up
    :param git_repo: a git repo link
    :param test_mode: a flag that makes this method spoof private/public keygen
    """
    if not test_mode:
        public_key, private_key = generate_ssh_keypair()
        secret_key = generate_printable_string(40)
        db_password = generate_printable_string(15, False)
    else:
        public_key = "PUBLIC_KEY"
        private_key = "PRIVATE_KEY"
        secret_key = "secret_key"
        db_password = "password"
    settings = {
        'git_repo': git_repo,
        'git_pub_key': public_key,
        'git_priv_key': private_key,
        'vagrant': {
            'db_host_ip': '127.0.0.1',
            'secret_key': secret_key,
            'settings_path': 'config.settings.local',
            'db_password': db_password
        }
    }
    if vault:
        registered_settings = register_values_in_vault('.',
                                                       'secret/git_keys_{}'.format(generate_printable_string(25,
                                                                                                             False)),
                                                       {'public_key': public_key, 'private_key': private_key},
                                                       quoted=True)
        settings['git_priv_key'] = registered_settings['private_key']
        settings['git_pub_key'] = registered_settings['public_key']
    return settings


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
    private = key.exportKey('PEM')
    if in_template:
        private = re.sub(r"\n", "\n  ", private)
    return public, private


def get_project_name_from_repo(repo_link, drop_hyphens=True):
    result = re.search(r"\.com[/:][^/]+/(.*)(\.git)?$", repo_link).group(1)
    result = re.sub(r"\.git$", "", result)
    if drop_hyphens:
        result = re.sub(r"\-", "", result)
    return result


def raw_input_wrapper(query, lower=False):
    try:
        usr_input = raw_input(query)
    except NameError:
        usr_input = input(query)
    if lower:
        usr_input = usr_input.lower()
    return usr_input


def pretty_print_dictionary(dictionary):
    print("{")
    try:
        dict_items = dictionary.iteritems()
    except AttributeError:
        dict_items = dictionary.items()
    for attr, value in dict_items:
        print("{0} : {1}, ".format(attr, value))
    print("}\n")


def get_vault_credentials_from_path(path):
    vaults = []
    vault_keys = {}
    for json_path in os.listdir(path):
        vault_query = re.search(r"vault_([^\.]+)\.json", json_path)
        if vault_query:
            vaults.append(vault_query.group(0))
        for idx, vault in enumerate(vaults):
            vault_keys[str(idx)] = vault
    print("Option:\tVault:")
    try:
        vault_keys_items = vault_keys.iteritems()
    except AttributeError:
        vault_keys_items = vault_keys.items()
    for option_num, vault in vault_keys_items:
        print("{0}:\t{1}".format(option_num, vault))
    try:
        vault_input = raw_input("Which vault do you want this server to access (use Option number)?:\t")
    except NameError:
        vault_input = input("Which vault do you want this server to access (use Option number)?:\t")
    vault_path = vault_keys[vault_input]
    with open(os.path.join(path, vault_path), 'r') as vault_file:
        vault_details = json.loads(vault_file.read())
        return vault_details["VAULT_ADDR"], vault_details["VAULT_TOKEN"], vault_path


def find_vagrantfile_dir(path=None):
    if path is None:
        path = os.getcwd()
    vagrantfile_path = os.path.join(path, "Vagrantfile")
    if os.path.exists(vagrantfile_path):
        return path
    if os.path.expanduser("~") == path:
        raise Exception('Vagrantfile not found! If running `yurt vault`, run `yurt vault --dest=.`')
    return find_vagrantfile_dir(os.path.dirname(path))


def register_values_in_vault(vagrantfile_path, vault_path, save_dict, quoted=False):
    url, token, path = get_vault_credentials_from_path(vagrantfile_path)
    client = hvac.Client(url=url, token=token)
    return_settings = {}
    try:
        if client.is_authenticated() and not client.is_sealed():
            client.write(vault_path, **save_dict)
            for key in save_dict:
                lookup_string = " ".join(("{{",
                                          "lookup('vault', '{0}', '{1}', '{2}')".format(vault_path,
                                                                                        key,
                                                                                        path),
                                          "}}"))
                if quoted:
                    lookup_string = "".join(("\\\"", lookup_string, "\\\""))
                return_settings[key] = lookup_string
            return return_settings
        else:
            raise Exception('Vault is unavailable!')
    except ConnectionError:
        print('Cannot connect to vault: Connection Error')


