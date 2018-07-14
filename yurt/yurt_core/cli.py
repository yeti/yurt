import click
from yurt.yurt_core.setup import setup
from yurt.yurt_core.env import env_vars


main = click.CommandCollection(sources=[
    setup,
    env_vars
])


if __name__ == '__main__':
    main()
