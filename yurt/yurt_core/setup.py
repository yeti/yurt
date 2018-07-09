# coding=utf-8
import os
import stat
import click
from builtins import input
from invoke import run
from yurt.yurt_core.utils import recursive_file_modify, generate_ssh_keypair, get_project_name_from_repo, add_settings
from yurt.yurt_core.paths import DJANGO_PROJECT_PATH, ORCHESTRATION_PROJECT_PATH, YURT_PATH, TEMPLATES_PATH
from cookiecutter.main import cookiecutter

__author__ = 'deanmercado'


def create_settings(vault, git_repo, test_mode=False):
    config_settings = add_settings(vault, git_repo, test_mode)
    project_name = get_project_name_from_repo(config_settings.get('git_repo'))
    config_settings['project_name'] = project_name
    config_settings['git_repo_url'] = config_settings.get('git_repo')
    config_settings['repo_name'] = get_project_name_from_repo(config_settings.get('git_repo'), False)
    return config_settings, project_name


def create_project(*args):
    """
    Creates Django project by copying over stuff
    """
    config_settings, project_name = args
    run("cp -rf {0} ./{1}".format(os.path.join(DJANGO_PROJECT_PATH, "*"), project_name))
    run("find . -name \"*.pyc\" -type f -delete")
    run("find . -name \"*.pyo\" -type f -delete")
    run("find . -name \"__pycache__\" -type f -delete")
    recursive_file_modify(os.path.abspath("./{0}".format(project_name)), config_settings)


def load_orchestration_and_requirements(*args):
    """
    Copies over the orchestration directory and requirements.txt file to current directory
    """
    config_settings, project_name = args
    run('cp -rf {0} ./{1}'.format(ORCHESTRATION_PROJECT_PATH, project_name))
    run('cp -f {0} ./{1}'.format(os.path.join(YURT_PATH, 'requirements.txt'), project_name))
    run('cp -f {0} ./{1}/.gitignore'.format(os.path.join(TEMPLATES_PATH, 'gitignore.template'), project_name))
    recursive_file_modify('./{0}/orchestration'.format(project_name), config_settings)


def enable_git_repo(*args):
    """
    Sets up git repository in project direcory
    """
    config_settings, project_name = args
    if project_name not in os.listdir('.'):
        run('mkdir {0}'.format(project_name))

    current_path = os.getcwd()
    os.chdir("./{}".format(project_name))
    run('git init', warn=True)
    run('git remote add origin {0}'.format(config_settings.get('git_repo_url')), warn=True)
    run('git checkout -b develop', warn=True)
    os.chdir(current_path)


def add_all_files_to_git_repo(*args):
    _, project_name = args
    current_path = os.getcwd()
    os.chdir("./{}".format(project_name))
    run('git add .')
    run('git commit -m "Project Start: Add general project structure and orchestration"')
    os.chdir(current_path)


def move_vagrantfile_to_project_dir(*args):
    """
    Moves Vagrantfile from `orchestration` directory to project directory
    """
    _, project_name = args
    run('mv ./{0}/orchestration/Vagrantfile .'.format(project_name))


def copy_ansible_configs_to_parent(*args):
    _, project_name = args
    run('cp {0}/ansible.cfg .'.format(project_name))


@click.group()
def setup():
    pass


@setup.command()
@click.option('--user', default=None, help='Remote SSH user')
@click.option('--host', default=None, help='SSH Host IP address')
@click.option('--key_name', default=None, help='Name of PEM file (in ~/.ssh)')
def copy_pem_file(user, host, key_name):
    """
    Appends public SSH Key to remote host
    """
    project_name = key_name

    if user is None:
        user = input("SSH User? (default: 'root'):\t")
        if user.strip(" ") == "":
            user = "root"
        else:
            user = user
    if host is None:
        host = input("Public IP/DNS of Remote Server?:\t")
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
            project_name = KEYNAME_ENUM[input("".join(("Which key in ~/.ssh are you ",
                                                       "copying to the remote server (Input the option)?:\t")))]
        except KeyError:
            raise KeyError("Not a good input!")
            return
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


@setup.command()
def new():
    """
    Create new project
    """
    template_location = 'gh:yeti/yurt_template-django'
    print('==> Creating a new project with Yurt Django 2.0 Template')
    cookiecutter(template_location)
    print('==> Project created: {}'.format(
        os.path.join(
            os.getcwd(),
            '<project_name>'
        )
    ))
    print('==> cd to the above path and run `docker-compose up`︎')


@setup.command()
@click.option('--git_repo', default=None, help='Git Repo Link')
@click.option('--git_branch', default='develop', help='Git Branch to checkout')
def existing(git_repo, git_branch):
    """
    Sets up existing project local environment
    """
    if git_repo is None:
        git_repo = input("""Enter the git repository link
        (i.e. git@github.com:mr_programmer/robot_repository.git):\t""")

    project_name = get_project_name_from_repo(git_repo)
    repo_name = get_project_name_from_repo(git_repo, False)
    SETTINGS = {
        'git_repo': git_repo,
        'project_name': project_name
    }
    run("git clone {0}".format(git_repo), warn=True)
    run("cd ./{} && git checkout {}".format(repo_name, git_branch), warn=True)
    if not(repo_name == project_name):
        run("mv ./{0} ./{1}".format(repo_name, project_name))
    run("cp {0} ./".format(os.path.join(ORCHESTRATION_PROJECT_PATH, "Vagrantfile")))
    run("cp {0} .".format(os.path.join(project_name, "ansible.cfg")))
    recursive_file_modify('./Vagrantfile', SETTINGS, is_dir=False)
    run("vagrant up")


if __name__ == '__main__':
    setup()
