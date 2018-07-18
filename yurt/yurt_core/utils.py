import os

import click

__author__ = 'deanmercado'

###
# helper functions
###


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


def yes_no_to_bool(value):
    if value.lower() == 'yes':
        return True
    elif value.lower() == 'no':
        return False
    else:
        raise ValueError('Invalid value: Use "yes" or "no".')


def echo_multiline(string):
    items = string.splitlines()
    for item in items:
        if '==>' in item:
            click.echo(item)
        else:
            click.secho(item, fg='green')

###
# helper classes
###


class Commands:

    __commands__ = {}
    subcommand = '[COMMAND]'

    def __init__(self, subcommands):
        for command_name, subcommand in subcommands:
            self.__commands__[command_name] = subcommand

    def invoke(self, command, *args):
        callable_command = self.__commands__.get(command, None)
        if callable_command is not None and callable(callable_command):
            try:
                return callable_command(*args)
            except TypeError:
                raise TypeError('`yurt {} {}` requires an argument. Run: yurt {} --help'.format(
                    self.subcommand,
                    command,
                    self.subcommand
                ))

        click.echo('yurt {} {}: Command doesn\'t exist. Run yurt {} --help'.format(
            self.subcommand,
            command,
            self.subcommand
        ))
