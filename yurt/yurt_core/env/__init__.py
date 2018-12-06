# coding=utf-8

import click
import os

from yurt.yurt_core.utils import find_file_in_ancestor
from .helpers import in_yurt_directory, EnvCommand
from .commands import add, import_func, export


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
