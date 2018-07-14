import click
from yurt.yurt_core.add import add
from yurt.yurt_core.deploy import deploy_cli
from yurt.yurt_core.setup import setup

main = click.CommandCollection(sources=[add, deploy_cli, setup])


if __name__ == '__main__':
    main()
