import os
from fabric.decorators import task
from fabric.operations import local
from fabric.context_managers import settings, lcd
from fabric.state import env
from fabric.tasks import execute
from context_managers import bash, ansible
from utils import recursive_file_modify, install_virtualenvwrapper, add_fab_path_to_bashrc, get_fab_settings, \
    generate_printable_string, generate_ssh_keypair

__author__ = 'deanmercado'

###
# fab setup commands: these commands setup a new django project
###


@task
def create_project():
    """
    Creates Django project by copying over
    :param proj_name: Name of the project
    :return: Void
    """
    env.settings = get_fab_settings()
    env.proj_name = env.settings.get('project_name')

    with bash():
        with lcd(env.proj_name):
            local("cp -rf $FAB_PATH/../django_project/* .")
        recursive_file_modify(os.path.abspath("./{}".format(env.proj_name)), env.settings)


@task
def create_ansible_env():
    """
    Creates the ansible environment
    :return: Void
    """
    with bash():
        with settings(warn_only=True):
            local('mkvirtualenv ansible')
    with ansible():
        with settings(warn_only=True):
            local('pip install ansible')
            local('ansible-galaxy install -r $FAB_PATH/../orchestration/roles/roles.txt')


@task
def load_orchestration_and_requirements():
    """
    Copies over the orchestration directory and requirements.txt file to current directory
    :return: Void
    """
    env.settings = get_fab_settings()
    env.proj_name = env.settings.get('project_name')

    with bash():
        local('cp -rf $FAB_PATH/../orchestration ./{}'.format(env.proj_name))
        local('cp -f $FAB_PATH/requirements.txt ./{}'.format(env.proj_name))
        recursive_file_modify('./{}/orchestration'.format(env.proj_name), env.settings)


@task
def enable_git_repo():
    """
    Sets up git repository in project direcory
    :return: Void
    """
    env.settings = get_fab_settings()
    env.proj_name = env.settings.get('project_name')

    if env.proj_name not in os.listdir('.'):
        local('mkdir {}'.format(env.proj_name))

    with lcd(env.proj_name):
        with settings(warn_only=True):
            local('git init')
            local('git remote add origin {}'.format(env.git_repo_url))
            local('git checkout -b develop')


@task
def move_vagrantfile_to_project_dir():
    env.settings = get_fab_settings()
    env.proj_name = env.settings.get('project_name')
    local('mv ./{}/orchestration/Vagrantfile .'.format(env.proj_name))


@task
def create_pem_file():
    env.settings = get_fab_settings()
    _, pem = generate_ssh_keypair(pem_only=True)
    project_name = env.settings.get('project_name')
    with open("./{}.pem".format(project_name), 'w') as key:
        key.write(pem)
        os.chmod("./{}.pem".format(project_name), 0400)

    print("".join(("PEM-file './{}.pem' added! Add this".format(project_name),
                   " to `~/.ssh/authorized_keys` of server.")))


@task
def delete_fabric_settings():
    local('rm fabric_settings.py*')


@task
def new():
    """
    Create new project
    :return: Void
    """
    env.settings = get_fab_settings()
    env.proj_name = env.settings.get('project_name')
    env.git_repo_url = env.settings.get('git_repo')
    install_virtualenvwrapper()
    add_fab_path_to_bashrc()

    execute(enable_git_repo)
    execute(create_project)
    execute(create_ansible_env)
    execute(load_orchestration_and_requirements)
    execute(move_vagrantfile_to_project_dir)
    execute(create_pem_file)
    execute(delete_fabric_settings)


@task
def add_settings():
    """
    Adds `fabric_settings.py` to this directory
    :return: Void
    """
    add_fab_path_to_bashrc()
    public_key, private_key = generate_ssh_keypair()
    SETTINGS = {
        'git_public_key': public_key,
        'git_private_key': private_key,
        'vagrant': {
            'db_pw': generate_printable_string(15),
            'secret_key': generate_printable_string(20)
        },
        'development': {
            'db_pw': generate_printable_string(15),
            'secret_key': generate_printable_string(20)
        },
        'staging': {
            'db_pw': generate_printable_string(15),
            'secret_key': generate_printable_string(20)
        },
        'production': {
            'db_pw': generate_printable_string(15),
            'secret_key': generate_printable_string(20)
        }
    }
    if 'fabric_settings.py' in os.listdir('.'):
        continue_process = raw_input('You already have `fabric_settings.py in this folder. Redo? (Y/N)')
        if continue_process.lower() == 'y':
            pass
        else:
            print("Aborted.")
            return False
    with bash():
        local('cp $FAB_PATH/fabric_settings.py.default.py ./fabric_settings.py')
        recursive_file_modify('./fabric_settings.py', SETTINGS, is_dir=False)
        print("".join(("You now have `fabric_settings.py`. Edit this file to have the correct ",
                       "values and then do `fab setup.new`")))
