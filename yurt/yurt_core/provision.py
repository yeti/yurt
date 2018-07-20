# coding=utf-8

import click
from invoke import run
from yurt.yurt_core.utils import Commands, yes_no_to_bool, echo_multiline


# Command Object


class ProvisionCommands(Commands):
    subcommand = 'provision'


# Helpers

def aws_ec2(is_dry_run):

    access_key = click.prompt('What is your AWS access key?')
    key_secret = click.prompt(' What is your AWS secret key?')
    name = click.prompt('What name will you give this remote host?')

    click.clear()

    invocation = """docker-machine create --driver amazonec2 \\
    --amazonec2-access-key {} \\
    --amazonec2-secret-key {} {}""".format(access_key, key_secret, name)

    command = run
    if is_dry_run:
        command = echo_multiline
        command('==> Run this command to provision Docker on a new EC2 Server:')

    command(invocation)

    return name


def generic(is_dry_run):
    ssh_key = click.prompt('What is the path to your ssh key for this host?',
                           default='~/.ssh/id_rsa',
                           show_default=True)
    ssh_ip_address = click.prompt(' What is the IP address for this host?')
    name = click.prompt('What name will you give this remote host?')

    click.clear()

    invocation = """docker-machine create --driver generic \\
    --generic-ip-address={} \\
    --generic-ssh-key {} {}""".format(ssh_ip_address, ssh_key, name)

    command = run
    if is_dry_run:
        command = echo_multiline
        command('==> Run this command to set up Docker on the remote host@{}'.format(ssh_ip_address))
    command(invocation)

    return name


# Commands

def new():
    is_new = click.prompt(
        'Just to confirm, are you preparing a new host with Docker? (yes/no)',
        value_proc=yes_no_to_bool,
        default='yes',
        show_default=True
    )
    if is_new:
        is_dry_run = click.prompt(
            'Dry-run? In other words, don\'t execute any code, just print the commands (yes/no)?',
            value_proc=yes_no_to_bool,
            default='yes',
            show_default=True
        )

        is_aws = click.prompt(
            'Do you wish to generate an AWS EC2 instance? (yes/no)',
            value_proc=yes_no_to_bool,
            default='yes',
            show_default=True
        )
        if is_aws:
            name = aws_ec2(is_dry_run)

        else:
            name = generic(is_dry_run)

        echo_multiline("""
==> Set up the environment variables for this host with the command below:
cd path/to/project
yurt env add

==> Deploy to the host
eval `docker-machine env {}`
docker-compose -f docker-compose.<env>.yml up

""".format(name))

    else:
        click.echo('Exiting!')


def existing():
    click.echo('==> Import the docker-machine config from the lead dev.')
    click.echo('==> We recommend using the following project to do so:')
    click.echo('==> https://github.com/bhurlow/machine-share')


# CLI Entrypoints

@click.group()
def provision_group():
    pass


@provision_group.command()
@click.argument('subcommand')
@click.argument('args', nargs=-1)
def provision(subcommand, args):
    """
    Provision new Docker-powered Hosts with Docker Machine

    Subcommands:

    👉 new - Provision a new remote host with Docker-Machine

    👉 existing - Import docker-machine configuration for an existing Docker host
    """
    commands = (
        ('new', new),
        ('existing', existing)
    )
    provision_commands = ProvisionCommands(commands)
    provision_commands.invoke(subcommand, *args)
