import os

from fabric.context_managers import settings
from fabric.decorators import task
from fabric.operations import local

__author__ = 'deanmercado'


@task
def deploy():
    """
    Starts deploy process
    :return:
    """
    ENVIRONMENT_OPTIONS = {}
    print "Option\tInventory"
    for index, filename in enumerate(os.listdir("./orchestration/inventory")):
        if not(filename == "vagrant"):
            try:
                ENVIRONMENT_OPTIONS[str(index)] = filename
                print "{0}:\t{1}".format(index, filename)
            except KeyError:
                print "Bad input! Try again"
                return

    with settings(warn_only=True):
        num_selection = raw_input("Which environment do you want to deploy (use Option number)?:\t")
        selection = ENVIRONMENT_OPTIONS[num_selection]
        local('ansible-playbook -i orchestration/inventory/{0} orchestration/site.yml'.format(selection))
