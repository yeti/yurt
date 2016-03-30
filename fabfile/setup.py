import os
from fabric.contrib.files import append
from fabric.decorators import task
from fabric.operations import local, run, put
from fabric.context_managers import settings, lcd
from fabric.state import env
from fabric.tasks import execute
from context_managers import bash
from utils import recursive_file_modify, add_fab_path_to_bashrc, get_fab_settings, \
    generate_printable_string, generate_ssh_keypair, get_environment_pem, get_project_name_from_repo

__author__ = 'deanmercado'

###
# fab setup commands: these commands setup a new django project
###


@task
def create_project():
    """
    Creates Django project by copying over
    :return: Void
    """
    env.settings = get_fab_settings()
    env.proj_name = get_project_name_from_repo(env.settings.get('git_repo'))
    env.settings['project_name'] = env.proj_name

    with bash():
        with lcd(env.proj_name):
            local("cp -rf $FAB_PATH/../django_project/* .")
        recursive_file_modify(os.path.abspath("./{}".format(env.proj_name)), env.settings)


@task
def load_orchestration_and_requirements():
    """
    Copies over the orchestration directory and requirements.txt file to current directory
    :return: Void
    """
    env.settings = get_fab_settings()
    env.proj_name = get_project_name_from_repo(env.settings.get('git_repo'))
    env.settings['project_name'] = env.proj_name

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
    env.proj_name = get_project_name_from_repo(env.settings.get('git_repo'))

    if env.proj_name not in os.listdir('.'):
        local('mkdir {}'.format(env.proj_name))

    with lcd(env.proj_name):
        with settings(warn_only=True):
            local('git init')
            local('git remote add origin {}'.format(env.git_repo_url))
            local('git checkout -b develop')


@task
def move_vagrantfile_to_project_dir():
    """
    Moves Vagrantfile from `orchestration` directory to project directory
    :return:
    """
    env.settings = get_fab_settings()
    env.proj_name = get_project_name_from_repo(env.settings.get('git_repo'))
    local('mv ./{}/orchestration/Vagrantfile .'.format(env.proj_name))


@task
def create_pem_file():
    """
    Generates an SSH Key Pair (that is added to your keychain and `~/.ssh` directory)
    :return:
    """
    env.settings = get_fab_settings()
    pub, pem = generate_ssh_keypair(in_template=False)
    project_name = get_project_name_from_repo(env.settings.get('git_repo'))

    with open("./{}.pem".format(project_name), 'w') as key:
        key.write(pem)
        os.chmod("./{}.pem".format(project_name), 0400)
        local("mv ./{}.pem ~/.ssh".format(project_name))
    with open("./{}.pub".format(project_name), 'w') as key:
        key.write(pub)
        local("mv ./{}.pub ~/.ssh".format(project_name))
        local("ssh-add ~/.ssh/{}.pem".format(project_name))
    print("PEM-file `~/.ssh/{}.pem` added!")


@task
def copy_pem_file(user=None, host=None, environment=None):
    """
    Appends public SSH Key (named after `project_name` in `fabric_settings.py`) to remote host
    :param user: str, Remote user
    :param host: str, Remote ip address
    :param environment: Dict, Environment Dictionary
    :return:
    """
    env.settings = get_fab_settings()
    env.user = user
    env.host_string = host
    project_name = get_project_name_from_repo(env.settings.get('git_repo'))

    if user is None:
        user = raw_input("SSH User? (default: 'root'):\t")
        if user.strip(" ") == "":
            env.user = "root"
        else:
            env.user = user
    if host is None:
        env.host_string = environment.get('app_host_ip')
    run('mkdir -p ~/.ssh')
    with open(os.path.expanduser('~/.ssh/{}.pub'.format(project_name)), 'r') as key:
        append("~/.ssh/authorized_keys", key.readline().rstrip("\n"))
    print("Pub key added to `/home/{}/.ssh/authorized_keys` in server".format(env.user))


@task
def delete_fabric_settings():
    """
    Deletes `fabric_settings.py`
    :return: None
    """
    backup_fab_settings = raw_input("Backup `fabric_settings.py` before it's deleted (Y/N)?")
    if backup_fab_settings.lower() == 'y':
        print 'Backing up `fabric_settings.py` => `fabric_settings.py.bak`'
        local('cp fabric_settings.py fabric_settings.py.bak')
    elif backup_fab_settings.lower() == 'n':
        print 'No backup made!'
    else:
        print 'Bad input. Re-run by calling `fab setup.delete_fabric_settings`'
        return None
    print 'Deleting `fabric_settings`'
    local('rm fabric_settings.py')
    local('rm *.pyc')


@task
def new(PEM_copy=None):
    """
    Create new project
    :return: Void
    """
    env.settings = get_fab_settings()
    env.proj_name = get_project_name_from_repo(env.settings.get('git_repo'))
    env.settings['project_name'] = env.proj_name
    env.git_repo_url = env.settings.get('git_repo')
    add_fab_path_to_bashrc()
    execute(enable_git_repo)
    execute(create_project)
    execute(load_orchestration_and_requirements)
    execute(move_vagrantfile_to_project_dir)
    if PEM_copy:
        execute(create_pem_file)
        environment = get_environment_pem(message='Export PEM file to remote')
        execute(copy_pem_file, environment=environment)
    delete_choice = {
        'y': True,
        'n': False
    }
    try:
        delete_setting = delete_choice[raw_input('''Delete `fabric_settings.py` file (Y/N)?
Hint: If you plan on running more fab calls after this, enter `N`.\nChoice:\t''').lower()]
    except KeyError:
        print "Bad input. `fabric_settings.py` not deleted."
        return None

    if delete_setting:
        execute(delete_fabric_settings)


@task
def existing():
    """
    Sets up existing project local environment
    :return:
    """
    add_fab_path_to_bashrc()
    git_repo = raw_input("Enter the git repository link\n(i.e. git@github.com:mr_programmer/robot_repository.git):\t")
    project_name = get_project_name_from_repo(git_repo)
    repo_name = get_project_name_from_repo(git_repo, False)
    env.settings = {
        'git_repo': git_repo,
        'project_name': project_name
    }
    local("git clone {}".format(git_repo))
    local("mv ./{} ./{}".format(repo_name, project_name))
    with bash():
        local("cp $FAB_PATH/../orchestration/Vagrantfile ./")
    recursive_file_modify('./Vagrantfile', env.settings, is_dir=False)
    local("vagrant up")


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
            'db_pw': generate_printable_string(15, False),
            'secret_key': generate_printable_string(20)
        },
        'development': {
            'db_pw': generate_printable_string(15, False),
            'secret_key': generate_printable_string(20)
        },
        'staging': {
            'db_pw': generate_printable_string(15, False),
            'secret_key': generate_printable_string(20)
        },
        'production': {
            'db_pw': generate_printable_string(15, False),
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
