import os
import click

from fabric.context_managers import settings, lcd
from fabric.contrib.files import append
from fabric.operations import local, run
from fabric.state import env
import hvac

from utils import recursive_file_modify, get_fab_settings, \
    generate_printable_string, generate_ssh_keypair, get_environment_pem, get_project_name_from_repo, \
    get_vault_credentials_from_path
from cli import main

__author__ = 'deanmercado'

YURT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
FABFILE_PATH = os.path.join(YURT_PATH, 'fabfile')
DJANGO_PROJECT_PATH = os.path.join(YURT_PATH, 'django_project')
ORCHESTRATION_PROJECT_PATH = os.path.join(YURT_PATH, 'orchestration')


def create_settings():
    fabric_settings = get_fab_settings()
    project_name = get_project_name_from_repo(fabric_settings.get('git_repo'))
    fabric_settings['project_name'] = project_name
    fabric_settings['git_repo_url'] = fabric_settings.get('git_repo')
    fabric_settings['repo_name'] = get_project_name_from_repo(fabric_settings.get('git_repo'), False)
    return fabric_settings, project_name


def create_project():
    """
    Creates Django project by copying over
    :return: Void
    """
    fabric_settings, project_name = create_settings()
    local("cp -rf {0} ./{1}".format(os.path.join(DJANGO_PROJECT_PATH, "*"), project_name))
    recursive_file_modify(os.path.abspath("./{0}".format(project_name)), fabric_settings)


def load_orchestration_and_requirements():
    """
    Copies over the orchestration directory and requirements.txt file to current directory
    :return: Void
    """
    fabric_settings, project_name = create_settings()
    local('cp -rf {0} ./{1}'.format(ORCHESTRATION_PROJECT_PATH, project_name))
    local('cp -f {0} ./{1}'.format(os.path.join(YURT_PATH, 'requirements.txt'), project_name))
    recursive_file_modify('./{0}/orchestration'.format(project_name), fabric_settings)


def enable_git_repo():
    """
    Sets up git repository in project direcory
    :return: Void
    """
    fabric_settings, project_name = create_settings()
    if project_name not in os.listdir('.'):
        local('mkdir {0}'.format(project_name))

    with lcd(project_name):
        with settings(warn_only=True):
            local('git init')
            local('git remote add origin {0}'.format(fabric_settings.get('git_repo_url')))
            local('git checkout -b develop')


def move_vagrantfile_to_project_dir():
    """
    Moves Vagrantfile from `orchestration` directory to project directory
    :return:
    """
    fabric_settings, project_name = create_settings()
    local('mv ./{0}/orchestration/Vagrantfile .'.format(project_name))


@main.command()
def create_pem_file():
    """
    Generates an SSH Key Pair (that is added to your keychain and `~/.ssh` directory)
    :return:
    """
    pub, pem = generate_ssh_keypair(in_template=False)

    project_name = raw_input("What will you name this ssh_key?\
    (Hint: just an alphanumeric name that describes what the key is for):\t")

    with open("./{0}.pem".format(project_name), 'w') as key:
        key.write(pem)
        os.chmod("./{0}.pem".format(project_name), 0400)
        local("mv ./{0}.pem ~/.ssh".format(project_name))
    with open("./{0}.pub".format(project_name), 'w') as key:
        key.write(pub)
        local("mv ./{0}.pub ~/.ssh".format(project_name))
        local("ssh-add ~/.ssh/{0}.pem".format(project_name))
    print("PEM-file `~/.ssh/{0}.pem` added!".format(project_name))


@main.command()
def copy_pem_file(user=None, host=None, key_name=None):
    """
    Appends public SSH Key (named after `project_name` in `fabric_settings.py`) to remote host
    :param user: str, Remote user
    :param host: str, Remote ip address
    :param key_name: str, Name of Key_pair in ~/.ssh
    :return:
    """
    project_name = key_name
    env.user = user
    env.host_string = host

    if user is None:
        user = raw_input("SSH User? (default: 'root'):\t")
        if user.strip(" ") == "":
            env.user = "root"
        else:
            env.user = user
    if host is None:
        env.host_string = raw_input("Public IP/DNS of Remote Server?:\t")
    if key_name is None:
        KEYNAME_ENUM = {}
        key_names = set([filename.split('.')[0]
                         if "." in filename
                         else filename
                         for filename in os.listdir(os.path.expanduser("~/.ssh"))])
        key_names.remove("config")
        print("Option\tKeyname")
        print("______\t_______")
        for index, keyname in enumerate(key_names):
            KEYNAME_ENUM[str(index)] = keyname
            print("{0}:\t{1}".format(index, keyname))
        print("")
        try:
            project_name = KEYNAME_ENUM[raw_input("".join(("Which key in ~/.ssh are you ",
                                                           "copying to the remote server (Input the option)?:\t")))]
        except KeyError:
            raise KeyError("Not a good input!")
            return
    print("If prompted for 'Passphrase for private key:', input the password credentials for this server.")
    run('mkdir -p ~/.ssh')
    with open(os.path.expanduser('~/.ssh/{0}.pub'.format(project_name)), 'r') as key:
        append("~/.ssh/authorized_keys", key.readline().rstrip("\n"))
    if env.user == "root":
        print("Pub key added to `/{0}/.ssh/authorized_keys` in server".format(env.user))
    else:
        print("Pub key added to `/home/{0}/.ssh/authorized_keys` in server".format(env.user))


def delete_fabric_settings():
    """
    Deletes `fabric_settings.py`
    :return: None
    """
    backup_fab_settings = raw_input("Backup `fabric_settings.py` before it's deleted (Y/N)?")
    if backup_fab_settings.lower() == 'y':
        print('Backing up `fabric_settings.py` => `fabric_settings.py.bak`')
        local('cp fabric_settings.py fabric_settings.py.bak')
    elif backup_fab_settings.lower() == 'n':
        print('No backup made!')
    else:
        print('Bad input.')
        return None
    print('Deleting `fabric_settings`')
    local('rm fabric_settings.py')
    local('rm *.pyc')


@main.command()
@click.pass_context
def new_project(context):
    """
    Create new project
    :return: None
    """
    enable_git_repo()
    create_project()
    load_orchestration_and_requirements()
    move_vagrantfile_to_project_dir()
    delete_choice = {
        'y': True,
        'n': False
    }
    local('vagrant up')
    try:
        delete_setting = delete_choice[raw_input('''Delete `fabric_settings.py` file (Y/N)?\nChoice:\t''').lower()]
    except KeyError:
        print("Bad input. `fabric_settings.py` not deleted.")
        return None

    if delete_setting:
        delete_fabric_settings()


@main.command()
def existing():
    """
    Sets up existing project local environment
    :return:
    """
    git_repo = raw_input("Enter the git repository link\n(i.e. git@github.com:mr_programmer/robot_repository.git):\t")
    project_name = get_project_name_from_repo(git_repo)
    repo_name = get_project_name_from_repo(git_repo, False)
    SETTINGS = {
        'git_repo': git_repo,
        'project_name': project_name
    }
    local("git clone {0}".format(git_repo))
    local("mv ./{0} ./{1}".format(repo_name, project_name))
    local("cp {0} ./".format(os.path.join(ORCHESTRATION_PROJECT_PATH, "Vagrantfile")))
    recursive_file_modify('./Vagrantfile', SETTINGS, is_dir=False)
    local("vagrant up")


@main.command()
@click.option('--vault', is_flag=True, help="Uses vault for git keys")
def add_settings(vault):
    """
    Adds `fabric_settings.py` to this directory
    :return: Void
    """
    public_key, private_key = generate_ssh_keypair()
    settings = {
        'git_public_key': public_key,
        'git_private_key': private_key,
        'vagrant': {
            'db_pw': generate_printable_string(15, False),
            'secret_key': generate_printable_string(40)
        }
    }
    if vault:
        url, token, path = get_vault_credentials_from_path(".")
        client = hvac.Client(url=url, token=token)
        if client.is_authenticated() and not client.is_sealed():
            unique_key = 'secret/git_keys_{}'.format(generate_printable_string(25, False))
            client.write(unique_key, private_key=private_key, public_key=public_key)
            settings['git_public_key'] = " ".join(["{{",
                                                   "lookup('vault', '{0}', 'public_key', '{1}')".format(unique_key,
                                                                                                        path),
                                                   "}}"])
            settings['git_private_key'] = " ".join(["{{",
                                                    "lookup('vault', '{0}', 'private_key', '{1}')".format(unique_key,
                                                                                                          path),
                                                    "}}"])
            print "Add this public key to your SSH deploy keys in Github:\n{}".format(public_key)
        else:
            raise Exception('Vault is unavailable!')
    if 'fabric_settings.py' in os.listdir('.'):
        continue_process = raw_input('You already have `fabric_settings.py in this folder. Overwrite? (Y/N)')
        if continue_process.lower() == 'y':
            pass
        else:
            print("Aborted.")
            return False
    local('cp {0} ./fabric_settings.py'.format(os.path.join(FABFILE_PATH, "fabric_settings.py.default.py")))
    recursive_file_modify('./fabric_settings.py', settings, is_dir=False)
    print("".join(("You now have `fabric_settings.py`. Edit this file to have the correct ",
                   "values and then enter `yurt new_project`")))
