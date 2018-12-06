# coding=utf-8
import json
import os
import re
from shutil import copytree, make_archive, rmtree
from zipfile import ZipFile

import click
from six import string_types

from yurt.yurt_core.utils import Commands, echo_multiline, get_iter


###
# Utils
###

class MachineShareCommands(Commands):
    subcommand = 'machine'


def check_for_target(target):
    if os.path.exists(target):
        return os.path.abspath(target)
    raise IOError('{} does not exist!'.format(os.path.abspath(target)))


def replace_home_path(source, _):
    return re.sub(os.path.expandvars('$HOME'), r'$HOME', source)


def replace_home_path_reverse(source, _):
    return re.sub(r'\$HOME', os.path.expandvars('$HOME'), source)


def replace_certs_path(source, machine_name):
    return re.sub(
        'machine/certs',
        'machine/machines/{}/certs'.format(machine_name),
        source)


def replace_sshkey(source, machine_name):
    return re.sub(
        r'\.ssh/(.*)$',
        r'.docker/machine/machines/{}/\1'.format(machine_name),
        source
    )


string_transform_pipeline = [
    replace_home_path,
    replace_certs_path,
    replace_sshkey
]


def transform_strings_with_machine_name(source, machine_name):
    result = source
    for transform in string_transform_pipeline:
        result = transform(result, machine_name)
    return result


def replace_values_with_home_var(dictionary, machine_name, reverse=False):
    for key, value in get_iter(dictionary):
        if isinstance(value, string_types):
            if reverse:
                dictionary[key] = replace_home_path_reverse(value, machine_name)
            else:
                dictionary[key] = transform_strings_with_machine_name(value, machine_name)
        elif type(value) is dict:
            dictionary[key] = replace_values_with_home_var(value, machine_name, reverse=reverse)
        else:
            dictionary[key] = value

    return dictionary


def change_config_json(config_json_path, machine_name, to_home=True):
    with open(config_json_path, 'r+') as config_json_stream:
        config_object = json.loads(config_json_stream.read())
        refined_object = replace_values_with_home_var(config_object, machine_name, reverse=(not to_home))
        config_json_stream.seek(0)
        config_json_stream.truncate()
        json.dump(refined_object, config_json_stream, indent=2)


###
# Commands
###

def export_machine(machine_name):
    dot_docker = check_for_target(os.path.expandvars('$HOME/.docker'))
    machine_path = os.path.join(dot_docker, 'machine')
    certs = os.path.join(machine_path, 'certs')

    target_machine = os.path.join(machine_path, 'machines', machine_name)
    check_for_target(target_machine)

    # Copy machine directory
    target_copy_dest = os.path.join(machine_path, 'machines', '{}.copy'.format(machine_name))
    copytree(target_machine, target_copy_dest)

    # Copy certs directory to target copy machine directory
    target_copy = check_for_target(target_copy_dest)
    cert_dest = os.path.join(target_copy, 'certs')
    copytree(certs, cert_dest)

    # Fix config.json
    config_json = check_for_target(
        os.path.join(
            target_copy,
            'config.json'
        )
    )

    change_config_json(config_json, machine_name)

    # Put in Zip File
    make_archive(machine_name, 'zip', target_copy)
    rmtree(target_copy)
    echo_multiline("""
==> Created `./{}.zip`
==> Share this with other machines to enable deploys on them
""".format(machine_name))


def import_machine(archive_path):
    archive_path = check_for_target(archive_path)
    base_name = os.path.splitext(os.path.basename(archive_path))[0]
    machines_path = os.path.expandvars('$HOME/.docker/machine/machines')
    if os.path.exists(machines_path):
        docker_machine_directory = os.path.join(machines_path, base_name)
        with ZipFile(archive_path) as zip_stream:
            zip_stream.extractall(docker_machine_directory)
        os.chdir(docker_machine_directory)
        change_config_json('./config.json', None, to_home=False)
        echo_multiline('''
==> Docker machine ({base_name}) imported!

===> Run (to activate):
eval $(docker-machine env {base_name})

'''.format(base_name=base_name))

###
# Entrypoints
###

@click.group()
def machine_share_group():
    pass


@machine_share_group.command()
@click.argument('subcommand')
@click.argument('args', nargs=-1)
def machine(subcommand, args):
    """
    (Experimental) Commands for Docker-Machine management and sharing

    Subcommands:

    👉 import [SRC] - Import docker-machine context to zip archive

    👉 export [FILENAME] - Export docker-machine context from zip archive
    """
    subcommands = (
        ('export', export_machine),
        ('import', import_machine)
    )
    machine_share_commands = MachineShareCommands(subcommands)
    machine_share_commands.invoke(subcommand, *args)
