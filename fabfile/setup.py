import os
from fabric.decorators import task
from fabric.operations import local
from fabric.context_managers import settings, lcd
from fabric.state import env
from fabric.tasks import execute
from context_managers import bash, ansible
from utils import recursive_file_modify, install_virtualenvwrapper, add_fab_path_to_bashrc

__author__ = 'deanmercado'

###
# fab setup commands: these commands setup a new django project
###


@task
def create_project(proj_name=None):
    """
    Creates Django project by copying over
    :param proj_name: Name of the project
    :return: Void
    """
    if proj_name:
        env.proj_name = proj_name

    try:
        env.settings = __import__("fabric_settings", globals(), locals(), [], 0).FABRIC
    except Exception:
        raise Exception('Create `fabric_settings.py` file in this directory')

    with lcd(env.proj_name):
        local("cp -rf $FAB_PATH/../django_project/* .")
        recursive_file_modify(os.path.abspath("."), env.settings)


@task
def create_ansible_env():
    """
    Creates the ansible environment
    :return: Void
    """
    with bash():
        local('mkvirtualenv ansible')
    with ansible():
        with settings(warn_only=True):
            local('pip install ansible')
            local('ansible-galaxy install -r $FAB_PATH/../orchestration/roles/roles.txt')


@task
def load_orchestration_and_requirements(proj_name=None):
    """
    Copies over the orchestration directory and requirements.txt file to current directory
    :return: Void
    """
    if proj_name:
        env.proj_name = proj_name

    try:
        env.settings = __import__("fabric_settings", globals(), locals(), [], 0).FABRIC
    except Exception:
        raise Exception('Create `fabric_settings.py` file in this directory')

    with bash():
        local('cp -rf $FAB_PATH/../orchestration ./{}'.format(env.proj_name))
        local('cp -f $FAB_PATH/requirements.txt ./{}'.format(env.proj_name))
        with lcd(os.path.join(env.proj_name, 'orchestration')):
            recursive_file_modify(os.path.abspath('.'))

        env.post_messages.append(" ".join(("Deployment step: Replace variables of YAML files in ",
                                           "`{}/orchestration/env_vars` and `{}/orchestration/inventory` with ",
                                           "desired values. Then run `fab deploy.deploy`")).format(env.proj_name,
                                                                                                   env.proj_name))


@task
def enable_git_repo(git_repo_url=None):
    """
    Sets up git repository in project direcory
    :return: Void
    """
    if git_repo_url:
        env.git_repo_url = git_repo_url
    with lcd(env.proj_name):
        local('git init')
        local('git remote add origin {}'.format(env.git_repo_url))
        local('git checkout -b develop')


@task
def new(proj_name, repo_url):
    """
    Create new project
    :param proj_name: Project name (string)
    :return: Void
    """

    env.proj_name = proj_name
    env.git_repo_url = repo_url
    env.post_messages = []
    install_virtualenvwrapper()
    add_fab_path_to_bashrc()

    execute(enable_git_repo)
    execute(create_project)
    execute(create_ansible_env)
    execute(load_orchestration_and_requirements)

    for message in env.post_messages:
        print message

@task
def add_settings():
    add_fab_path_to_bashrc()
    if 'fabric_settings.py' in os.listdir():
        continue_process = raw_input('You already have `fabric_settings.py in this folder. Redo? (Y/N)')
        if continue_process.lower() == 'y':
            pass
        else:
            print "Aborted."
            return False
    with bash():
        local('cp $FAB_PATH/fabric_settings.py.default.py ./fabric_settings.py')
        print "".join(("You now have `fabric_settings.py`. Edit this file to have the correct ",
                       "values and then do `fab setup.new:<proj_name>,<git_repo_url>"))