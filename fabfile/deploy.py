import os
from fabric.decorators import task
from fabric.operations import local
from contextlib import contextmanager
from fabric.context_managers import prefix

__author__ = 'deanmercado'

###
# Context Managers
###


@contextmanager
def bash():
    with prefix('source ~/.bashrc'):
        yield


@contextmanager
def ansible():
    with prefix('workon ansible'):
        yield

###
# Hidden/Helper functions
###


def _install_virtualenvwrapper():
    """
    Installs virtualenvwrapper globally, adding to $HOME/.bashrc the required lines
    :return: Void
    """
    try:
        local('sudo pip install virtualenvwrapper')
    except Exception, e:
        print 'virtualenvwrapper already installed'

    if not os.path.exists("$HOME/.added_virtualenvwrapper_to_bashrc"):
        local('echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc')
        local('echo "export PROJECT_HOME=$HOME/Devel" >> ~/.bashrc')
        local('echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc')
        local("touch $HOME/.added_to_bashrc")


@task
def add_fab_path_to_bashrc():
    """
    Adds FAB_PATH variable to .bashrc
    :return: Void
    """
    with prefix('cd fabfile'):
        if not os.path.exists("$HOME/.added_fabpath_to_bashrc"):
            local('echo "export FAB_PATH=$(pwd -P)" >> ~/.bashrc')

###
# Commands that could be called through fab
###


@task
def create_ansible_env():
    """
    Creates the ansible environment if it hasn't been created already
    :return: Void
    """
    try:
        _install_virtualenvwrapper()
    except Exception, e:
        print str(e)
    try:
        bash('mkvirtualenv ansible')
        ansible('pip install ansible')
    except Exception, e:
        print "Ansible environment exists already!"


def load_orchestration():
    """
    Copies orchestration directory to current directory
    :return:
    """
    local('cp -rf ./orchestration ../')


@task
def new():
    pass