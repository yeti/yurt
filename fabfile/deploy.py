from contextlib import contextmanager
import os
from subprocess import call
from fabric.decorators import task
from fabric.operations import local
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
    with bash():
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
        local('pip install virtualenvwrapper')
    except Exception, e:
        print 'virtualenvwrapper already installed'
    if not os.path.exists(os.path.expanduser("~/.added_virtualenvwrapper_to_bashrc")):
        local('echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc')
        local('echo "export PROJECT_HOME=$HOME/Devel" >> ~/.bashrc')
        local('echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc')
        local("touch $HOME/.added_virtualenvwrapper_to_bashrc")


def _add_fab_path_to_bashrc():
    """
    Adds FAB_PATH variable to .bashrc
    :return: Void
    """
    with prefix('cd fabfile'):
        if not os.path.exists(os.path.expanduser("~/.added_fabpath_to_bashrc")):
            local('echo "export FAB_PATH=$(pwd -P)" >> ~/.bashrc')
            local("touch $HOME/.added_fabpath_to_bashrc")

###
# Commands that could be called through fab
###


@task
def create_ansible_env():
    """
    Creates the ansible environment
    :return: Void
    """
    try:
        _install_virtualenvwrapper()
        _add_fab_path_to_bashrc()
    except Exception, e:
        print str(e)
    with bash():
        local('mkvirtualenv ansible')
    with ansible():
        local('pip install ansible')
        try:
            local('ansible-galaxy install -r $FAB_PATH/../orchestration/roles/roles.txt')
        except Exception:
            pass


@task
def load_orchestration():
    """
    Copies orchestration directory to current directory
    :return:
    """
    with bash():
        local('cp -rf $FAB_PATH/../orchestration ./')
        print "Replace variables in YAML files in `orchestration/env_vars` with desired values."


@task
def new():
    pass