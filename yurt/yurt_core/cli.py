import click


@click.group()
def main():
    pass

from yurt.yurt_core.setup import new_project, create_pem_file, copy_pem_file, existing
from yurt.yurt_core.add import remote_server, vault
from yurt.yurt_core.deploy import deploy

if __name__ == '__main__':
    main()
