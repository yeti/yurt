# coding=utf-8

import click
import os
import re
import yaml
from cookiecutter.main import cookiecutter
from shutil import copy2, make_archive
from yurt.yurt_core.utils import get_iter, find_file_in_ancestor
from zipfile import ZipFile


# Helpers

def in_yurt_directory():
    return os.path.exists('./docker-compose.yml') and \
           os.path.exists('./django_app') and \
           os.path.exists('./envs')


def add():
    # Create env var file in envs
    os.chdir('./envs')
    result_path = cookiecutter('gh:yeti/yurt_template-envvars')
    environment = re.search(r'envs/(.+)\.env\.d$', result_path).group(1)

    # Copy docker-compose.remote.yml
    os.chdir('..')
    target_file = './docker-compose.{}.yml'.format(environment)
    copy2(
        './docker-compose.remote.yml',
        './docker-compose.{}.yml'.format(environment)
    )

    # Edit copy with new env vars
    with open(target_file, 'r+') as target_file_obj:
        compose_contents = yaml.load(target_file_obj.read())
        target_file_obj.seek(0)
        target_file_obj.truncate()
        env_file = './envs/{}.env'.format(environment)

        all_services = compose_contents.get('services', {})
        for key, _ in get_iter(all_services):
            all_services[key]['env_file'] = [env_file]
        compose_contents['services'] = all_services
        yaml.dump(compose_contents, target_file_obj, default_flow_style=False)


def import_func(src):
    click.echo('==> Extracting {} into ./envs'.format(src))
    with ZipFile(src) as zip_stream:
        zip_stream.extractall('./envs')
    click.echo('==> Success!')


def export(filename):
    click.echo('==> Exporting .envs/ into ./{}.zip'.format(filename))
    make_archive(filename, 'zip', './envs')
    click.echo('==> Success!')
    click.echo('==> Upload this zip archive to a vault. To import:')
    click.echo('👉  yurt env import <path-to-archive>')


class EnvCommand:

    __commands__ = {}

    def __init__(self, subcommands):
        for command_name, subcommand in subcommands:
            self.__commands__[command_name] = subcommand

    def invoke(self, command, *args):
        callable_command = self.__commands__.get(command, None)
        if callable_command is not None and callable(callable_command):
            return callable_command(*args)
        click.echo('yurt env {}: Command doesn\'t exist. Run yurt env --help'.format(command))


# Actual Commands

@click.group()
def env_vars():
    pass


@env_vars.command()
@click.argument('subcommand')
@click.argument('args', nargs=-1)
def env(subcommand, args):
    """
    Manage Environment Variable Files in your project

    Subcommands:

    👉 add - Add a new *.env file to ./envs and a new docker-compose.*.yml file

    👉 import [SRC] - Import *.env files from {SRC}.zip to ./envs

    👉 export [FILENAME] - Export *.env files from ./envs to {FILENAME}.zip
    """
    if not in_yurt_directory():
        docker_compose_path = find_file_in_ancestor(
            'docker-compose.yml',
            stack_limit=3,
            error_message='Could not find `docker-compose.yml` in this path. Are you in a project directory?'
        )
        os.chdir(docker_compose_path)
    all_commands = [
        ('add', add),
        ('import', import_func),
        ('export', export)
    ]
    env_commands = EnvCommand(all_commands)
    env_commands.invoke(subcommand, *args)
