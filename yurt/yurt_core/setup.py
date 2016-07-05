import os
import click
from invoke import run
from utils import recursive_file_modify, \
    generate_ssh_keypair, get_project_name_from_repo, add_settings
from cli import main

__author__ = 'deanmercado'

YURT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DJANGO_PROJECT_PATH = os.path.join(YURT_PATH, 'django_project')
ORCHESTRATION_PROJECT_PATH = os.path.join(YURT_PATH, 'orchestration')
FABFILE_PATH = os.path.join(YURT_PATH, 'yurt_core')


def create_settings(vault, git_repo):
    config_settings = add_settings(vault, git_repo)
    project_name = get_project_name_from_repo(config_settings.get('git_repo'))
    config_settings['project_name'] = project_name
    config_settings['git_repo_url'] = config_settings.get('git_repo')
    config_settings['repo_name'] = get_project_name_from_repo(config_settings.get('git_repo'), False)
    return config_settings, project_name


def create_project(config_settings, project_name):
    """
    Creates Django project by copying over stuff
    """
    run("cp -rf {0} ./{1}".format(os.path.join(DJANGO_PROJECT_PATH, "*"), project_name))
    recursive_file_modify(os.path.abspath("./{0}".format(project_name)), config_settings)


def load_orchestration_and_requirements(config_settings, project_name):
    """
    Copies over the orchestration directory and requirements.txt file to current directory
    """
    run('cp -rf {0} ./{1}'.format(ORCHESTRATION_PROJECT_PATH, project_name))
    run('cp -f {0} ./{1}'.format(os.path.join(YURT_PATH, 'requirements.txt'), project_name))
    run('cp -f {0} ./{1}/.gitignore'.format(os.path.join(FABFILE_PATH, 'gitignore.template'), project_name))
    recursive_file_modify('./{0}/orchestration'.format(project_name), config_settings)


def enable_git_repo(config_settings, project_name):
    """
    Sets up git repository in project direcory
    """
    if project_name not in os.listdir('.'):
        run('mkdir {0}'.format(project_name))

    current_path = os.getcwd()
    os.chdir("./{}".format(project_name))
    run('git init', warn=True)
    run('git remote add origin {0}'.format(config_settings.get('git_repo_url')), warn=True)
    run('git checkout -b develop', warn=True)
    os.chdir(current_path)


def add_all_files_to_git_repo(config_settings, project_name):
    current_path = os.getcwd()
    os.chdir("./{}".format(project_name))
    run('git add .')
    run('git commit -m "Project Start: Add general project structure and orchestration"')
    os.chdir(current_path)


def move_vagrantfile_to_project_dir(config_settings, project_name):
    """
    Moves Vagrantfile from `orchestration` directory to project directory
    """
    run('mv ./{0}/orchestration/Vagrantfile .'.format(project_name))


@main.command()
def create_pem_file():
    """
    Generates an SSH Key Pair (that is added to your keychain and `~/.ssh` directory)
    """
    pub, pem = generate_ssh_keypair(in_template=False)

    project_name = raw_input("What will you name this ssh_key?\
    (Hint: just an alphanumeric name that describes what the key is for):\t")

    with open("./{0}.pem".format(project_name), 'w') as key:
        key.write(pem)
        os.chmod("./{0}.pem".format(project_name), 0400)
        run("mv ./{0}.pem ~/.ssh".format(project_name))
    with open("./{0}.pub".format(project_name), 'w') as key:
        key.write(pub)
        run("mv ./{0}.pub ~/.ssh".format(project_name))
        run("ssh-add ~/.ssh/{0}.pem".format(project_name))
    print("PEM-file `~/.ssh/{0}.pem` added!".format(project_name))


@main.command()
@click.option('--user', default=None, help='Remote SSH user')
@click.option('--host', default=None, help='SSH Host IP address')
@click.option('--key_name', default=None, help='Name of PEM file (in ~/.ssh)')
def copy_pem_file(user, host, key_name):
    """
    Appends public SSH Key to remote host
    """
    project_name = key_name

    if user is None:
        user = raw_input("SSH User? (default: 'root'):\t")
        if user.strip(" ") == "":
            user = "root"
        else:
            user = user
    if host is None:
        host = raw_input("Public IP/DNS of Remote Server?:\t")
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
    with open(os.path.expanduser('~/.ssh/{0}.pub'.format(project_name)), 'r') as key:
        # Copy the key over to the server's authorized keys
        run('ssh {}@{} "mkdir -p ~/.ssh && echo \"{}\" >> ~/.ssh/authorized_keys"'.format(user,
                                                                                          host,
                                                                                          key.readline().strip('\n')),
            warn=True)
    if user == "root":
        print("Pub key added to `/{0}/.ssh/authorized_keys` in server".format(user))
    else:
        print("Pub key added to `/home/{0}/.ssh/authorized_keys` in server".format(user))


@main.command()
@click.option('--git_repo', default=None, help='Git Repo Link')
@click.option('--vault', is_flag=True, help="Uses vault for git keys")
def new_project(git_repo, vault):
    """
    Create new project
    """
    if git_repo is None:
        git_repo = raw_input("".join(("Enter the git repository link\n",
                                      "(i.e. git@github.com:mr_programmer/robot_repository.git):\t")))
    ordered_methods = [
        enable_git_repo,
        create_project,
        load_orchestration_and_requirements,
        move_vagrantfile_to_project_dir,
        add_all_files_to_git_repo
    ]
    args = create_settings(vault, git_repo)
    # TODO: Validate `args` before running them through THE GAUNTLET
    for method in ordered_methods:
        method(*args)
    run('vagrant up')


@main.command()
@click.option('--git_repo', default=None, help='Git Repo Link')
def existing(git_repo):
    """
    Sets up existing project local environment
    """
    if git_repo is None:
        git_repo = raw_input("""Enter the git repository link
        (i.e. git@github.com:mr_programmer/robot_repository.git):\t""")
    project_name = get_project_name_from_repo(git_repo)
    repo_name = get_project_name_from_repo(git_repo, False)
    SETTINGS = {
        'git_repo': git_repo,
        'project_name': project_name
    }
    run("git clone {0}".format(git_repo))
    run("mv ./{0} ./{1}".format(repo_name, project_name))
    run("cp {0} ./".format(os.path.join(ORCHESTRATION_PROJECT_PATH, "Vagrantfile")))
    recursive_file_modify('./Vagrantfile', SETTINGS, is_dir=False)
    run("vagrant up")


if __name__ == '__main__':
    main()
