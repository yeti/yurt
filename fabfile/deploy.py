from fabric.context_managers import settings
from fabric.decorators import task
from fabric.operations import local
from context_managers import ansible, in_project

__author__ = 'deanmercado'

@task
def deploy(environment):
    with ansible():
        with in_project():
            with settings(warn_only=True):
                local('ansible-playbook -i orchestration/inventory/{}'.format(environment))
