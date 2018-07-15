import click
import os


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


# Helpers

def in_yurt_directory():
    return os.path.exists('./docker-compose.yml') and \
           os.path.exists('./django_app') and \
           os.path.exists('./envs')
