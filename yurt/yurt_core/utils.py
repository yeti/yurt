import json
import string
import hvac
from Crypto.PublicKey import RSA
import re
from random import choice
from requests import ConnectionError
import os
import yaml

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
        try:
            file_text = re.sub(var_pattern, target_dictionary.get(variable), file_text)
        except TypeError:
            print('Variable %({})s not sourced. Unfilled variable left in file {}.'.format(variable, filepath))
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
    result = re.search(r"\.\w{2,3}[/:][^/]+/(.*)(\.git)?$", repo_link).group(1)
    result = re.sub(r"\.git$", "", result)
    if drop_hyphens:
        result = re.sub(r"\-", "", result)
    return result

def get_owner_name_from_repo(repo_link):
    result = re.search(r"\.com[/:]([^/]+)/.*(\.git)?$", repo_link).group(1)
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


def find_project_folder(path=None):
    if path is None:
        path = os.getcwd()
    vagrantfile_path = os.path.abspath(find_vagrantfile_dir(path))
    path_files = []
    for child_path in os.listdir(vagrantfile_path):
        path_files.append(os.path.join(vagrantfile_path, child_path))
    project_path = None
    for path_file in path_files:
        if os.path.isdir(path_file) and 'manage.py' in os.listdir(path_file):
            project_path = path_file
    return project_path


def find_file_in_ancestor(
        target_file,
        path=None,
        error_message='Could not find file in ancestor',
        stack_limit=None,
        depth=0
):
    if path is None:
        path = os.getcwd()
    if os.path.exists(os.path.join(path, target_file)):
        return path
    if stack_limit is None:
        if os.path.expanduser("~") == path:
            raise IOError(error_message)
    if stack_limit:
        if depth == stack_limit:
            raise IOError("{}: Max stack limit reached".format(error_message))

    return find_file_in_ancestor(
        target_file,
        path=os.path.dirname(path),
        error_message=error_message,
        stack_limit=stack_limit,
        depth=depth + 1
    )


def find_vagrantfile_dir(path=None):
    return find_file_in_ancestor("Vagrantfile", path)


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


def go_over_questions(question_dict, current_value_dict, result=None, defaults=None):
    """
    :param: question_dict (OrderedDict): Dictionary of key -> question
    :param: current_value_dict (OrderedDict): Dictionary of current key-value pairs
    :param: result (Dict): The result dictionary
    :param: defaults (Dict or CallDict): Defaults for values that yield empty user inputs (optional)
    :return: (Dict)
    """
    if result is None:
        result = {}
    question_items = get_iter(question_dict)
    for attribute, prompt in question_items:
        if current_value_dict[attribute] is None:
            user_response = raw_input_wrapper(prompt, True)
            if user_response == '':
                if defaults is not None:
                    result[attribute] = defaults.get(attribute)
            else:
                result[attribute] = user_response
        else:
            result[attribute] = current_value_dict[attribute]
    return result


def generate_dict_of_things(label="things"):
    """
    :param label: (String)
    :return: (Dict)
    """
    thing_dict = {}
    key = None
    value = None
    try:
        while True:
            print("To quit generating {}, press (CTRL/CMD)+c ".format(label) +
                  "or press Enter when prompted for \"Key\"")
            key = raw_input_wrapper("Key?: ")
            if key == "":
                return thing_dict
            value = raw_input_wrapper("Value?: ")
            try:
                # If Value is an object, validate
                value = json.loads(value)
            except ValueError:
                pass
            thing_dict[str(key)] = value
            print("Current dictionary of {}:".format(label))
            pretty_print_dictionary(thing_dict)
    except KeyboardInterrupt:
        if key is None or value is None:
            # Proceed with keyboard interrupt
            raise KeyboardInterrupt()
        else:
            return thing_dict


def get_iter(dictionary):
    """
    Just a wrapper method that handles Python2->Python3 dict iterations
    :param dictionary: (Dict)
    :return: (Dict)
    """
    try:
        return dictionary.iteritems()
    except AttributeError:
        return dictionary.items()


def generate_options(options, item_label='Item', exclude=None):
    """
    :param options: (List)
    :param item_label: (String)
    :param exclude: (List)
    :return: (Tuple (String, Dict))
    """
    if exclude is None:
        exclude = []
    result_dict = {}
    result = "Option\t{}".format(item_label)
    for index, option in enumerate(options):
        if option not in exclude:
            result_dict[str(index)] = option
            result = "\n".join((result, "{}\t{}".format(index, option)))
    return result, result_dict


def add_key_value_to_yaml(yaml_path, key_values, **other_dump_attributes):
    """
    :param yaml_path: (String)
    :param key_values: (Dict)
    :param other_dump_attributes: (**kwargs)
    :return: None
    """
    with open(yaml_path, "a") as yaml_file:
        # Appends result to the yaml_file
        yaml_file.write(yaml.safe_dump(
            key_values,
            default_flow_style=False,
            **other_dump_attributes
        ))


def get_value_from_yaml(yaml_path, key, default=None):
    """
    :param yaml_path: (String)
    :param key: (String)
    :param default: (Any)
    :return: Any
    """
    with open(yaml_path, "r") as yaml_file:
        return yaml.load(yaml_file.read()).get(key, default)


def remove_value_from_yaml(yaml_path, key):
    """
    :param yaml_path: (String)
    :param key: (String)
    :return: Any
    """
    with open(yaml_path, "r") as yaml_file_read:
        current_yaml = yaml.load(yaml_file_read.read())
    result = current_yaml[key]
    del current_yaml[key]
    with open(yaml_path, "w") as yaml_file_write:
        yaml_file_write.write(yaml.safe_dump(
            current_yaml,
            default_flow_style=False,
            explicit_start=True
        ))
    return result


class DeferredCallable(object):

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def call(self):
        return self._func(*self._args, **self._kwargs)


class CallDict(dict):

    def get(self, key, default=None):
        value = super(CallDict, self).get(key, default)
        if isinstance(value, DeferredCallable):
            value = value.call()
        return value
