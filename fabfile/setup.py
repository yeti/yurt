import os
from fabric.decorators import task
from fabric.operations import local
from fabric.context_managers import prefix, settings
from fabric.state import env
from fabric.tasks import execute
from context_managers import bash, venv, ansible

__author__ = 'deanmercado'

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
def create_project(proj_name=None):
    """
    Creates Django project
    :param project_name: Name of the project
    :return: Void
    """
    if proj_name:
        env.proj_name = proj_name
    with bash():
        local('mkvirtualenv %s' % env.proj_name)
    with venv(env.proj_name):
        local('pip install -r $FAB_PATH/requirements.txt')
        with prefix('export PATH=$WORKON_HOME/%s/bin:$PATH' % env.proj_name):
            local('python $WORKON_HOME/%s/bin/django-admin.py startproject %s' % (env.proj_name, env.proj_name))


@task
def create_ansible_env():
    """
    Creates the ansible environment
    :return: Void
    """

    with bash():
        local('mkvirtualenv ansible')
    with ansible():
        local('pip install ansible')
        with settings(warn_only=True):
            local('ansible-galaxy install -r $FAB_PATH/../orchestration/roles/roles.txt')


@task
def load_orchestration_and_requirements(proj_name=None):
    """
    Copies over the orchestration directory and requirements.txt file to current directory
    :return: Void
    """
    if proj_name:
        env.proj_name = proj_name
    with bash():
        local('cp -rf $FAB_PATH/../orchestration ./%s' % env.proj_name)
        local('cp -f $FAB_PATH/requirements.txt ./%s' % env.proj_name)
        env.post_messages.append(" ".join(("Deployment step: Replace variables of YAML files in ",
                                           "`%s/orchestration/env_vars` with " % env.proj_name,
                                           "desired values. Then run `fab deploy`")))


@task
def new(proj_name):
    """
    Create new project
    :param proj_name: Project name (string)
    :return: Void
    """

    env.proj_name = proj_name
    env.post_messages = []
    _install_virtualenvwrapper()
    _add_fab_path_to_bashrc()

    execute(create_project)
    execute(create_ansible_env)
    execute(load_orchestration_and_requirements)

    for message in env.post_messages:
        print message
