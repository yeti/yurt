# Testing Util Methods
import os
from ..setup import create_settings


def assemble_call_args_list(subcommand, kwargs_dict={}):
    result = [subcommand, ]
    try:
        dict_items = kwargs_dict.iteritems()
    except AttributeError:
        dict_items = kwargs_dict.items()

    for key, value in dict_items:
        result.append("".join(("--", key)))
        if value:
            result.append(value)
    return result


def yield_vault_inputs(prompt):
    if 'ssl' in prompt:
        return 'True'
    if 'IP/DNS' in prompt:
        return '1.2.3.4'
    if 'token' in prompt:
        return 'ea4d-ff43-1200-b32f'
    if 'name' in prompt:
        return 'test_vault'
    if 'Enter' in prompt:
        return ''


def fake_open_file(*args):
    return "file at: {}, {}".format(*args)


def testmode_create_settings(vault, git_repo):
    settings, name = create_settings(vault, git_repo, True)
    return settings, name


def fake_abspath(path):
    current_path_components = os.path.split(path)
    if current_path_components[0] == ".":
        path = current_path_components[1:]
    else:
        path = current_path_components
    return "/" + os.path.join('fake', 'abspath', *path)
