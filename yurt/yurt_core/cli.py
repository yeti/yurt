import click

from yurt.yurt_core.machine_share import machine_share_group
from yurt.yurt_core.provision import provision_group
from yurt.yurt_core.setup import setup
from yurt.yurt_core.env import env_vars


main = click.CommandCollection(sources=[
    setup,
    env_vars,
    provision_group,
    machine_share_group
])
