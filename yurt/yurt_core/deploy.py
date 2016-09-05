import click
import os
from invoke import run

__author__ = 'deanmercado'


@click.group()
def deploy_cli():
    pass


@deploy_cli.command()
def deploy():
    """
    Starts deploy process
    :return:
    """
    ENVIRONMENT_OPTIONS = {}
    if not os.path.exists("orchestration"):
        print("You aren't in a Yurt repository yet. Use `cd` to get in the right directory.")
        return

    print("Option\tInventory")
    for index, filename in enumerate(os.listdir("./orchestration/inventory")):
        if not(filename == "vagrant"):
            ENVIRONMENT_OPTIONS[str(index)] = filename
            print("{0}:\t{1}".format(index, filename))
    num_selection = raw_input("Which environment do you want to deploy (use Option number)?:\t")
    selection = ENVIRONMENT_OPTIONS[num_selection]
    run('ansible-playbook -i orchestration/inventory/{0} orchestration/site.yml'.format(selection))

if __name__ == '__main__':
    deploy_cli()
