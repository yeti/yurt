import json
import os
from collections import OrderedDict
import click
import hvac
from fabric.context_managers import lcd
from fabric.operations import local
from requests import ConnectionError

from cli import main
from setup import YURT_PATH
from utils import get_project_name_from_repo, generate_printable_string,\
                  recursive_file_modify, raw_input_wrapper, pretty_print_dictionary, \
                  get_vault_credentials_from_path, generate_ssh_keypair, find_vagrantfile_dir, \
                  register_values_in_vault

TEMPLATES_PATH = os.path.join(YURT_PATH, "templates")
FABFILE_PATH = os.path.join(YURT_PATH, 'fabfile')


ATTRIBUTE_TO_QUESTION_MAPPING = OrderedDict([
    ("git_repo", "Enter the git repository link\n(i.e. git@github.com:mr_programmer/robot_repository.git):\t"),
    ("env", "What name is this environment (i.e. development, staging, production)?: "),
    ("abbrev_env", "How do you want this environment abbreviated (i.e. dev, stage, prod)?: "),
    ("app_host_ip", "What is the public DNS of this project's host (i.e. example.com)?: "),
    ("db_host_ip", "What is this project's DB host (Hint: public IP of project if hosted locally)?: "),
    ("debug", "This Django server will use Debug mode (True/False): "),
    ("num_gunicorn_workers", "".join(("How many gunicorn workers do you want ",
                                      "(Hint: For the number of workers, a go",
                                      "od rule to follow is 2 x number of CPUs + 1)?: "))),
    ("gunicorn_max_requests", "".join(("What do you want to set `gunicorn_max_requests` to ? ",
                                       "Setting this to 1 will restart the Gunicorn process each time ",
                                       "you make a request, basically reloading the code. Very han",
                                       "dy when developing. Set to 0 for unlimited requests.: "))),
    ("ssl_enabled", "Is SSL enabled on this server (yes/no)?: "),
    ("git_branch", "From which git branch will the server pull the project?: "),
    ("vault_used", "Are you utilizing a vault to store secrets for this server (yes/no)?: ")
])

VAULT_ATTRIBUTES_TO_QUESTIONS = OrderedDict([
    ("PROTOCOL", "Is this vault ssl enabled (True/False)?: "),
    ("VAULT_ADDR", "What is the public IP/DNS of this vault (ex. example.com)?: "),
    ("VAULT_TOKEN", "What is your token for this vault?: "),
    ("VAULT_UUID", "What will you name this vault (leave blank for random)?: ")
])

TEMPLATE_TO_PROJECT_MAPPING = {
    "./env_settings.py.template.py": "{0}/{1}/config/settings/{2}.py",
    "./env_vars.yml.template": "{0}/{1}/orchestration/env_vars/{3}.yml",
    "./inventory.template": "{0}/{1}/orchestration/inventory/{3}"
}

SECRETS_PARAMS = [
    "secret_key",
    "db_password"
]


@main.command()
def remote_server():
    """
    Adds remote server files for deploying to new remote servers
    """
    if os.path.exists("./templates.tmp"):
        print("A `templates.tmp` directory is in the current working directory. Delete this before trying again.")
        return None
    lowercase_attrs = ["env", "abbrev_env"]
    settings = {
        "secret_key": generate_printable_string(40),
        "db_password": generate_printable_string(20, False),
    }

    raw_input("You will be asked a bunch of questions for setting up the server.\nMake sure your "
              "input is as accurate as possible.\nIf given a choice in parentheses, make sure\n"
              "the input you enter matches one of those choices.\n"
              "Press Enter to Continue.")

    for attribute, prompt in ATTRIBUTE_TO_QUESTION_MAPPING.iteritems():
        settings[attribute] = raw_input_wrapper(prompt, attribute in lowercase_attrs)
    vagrantfile_path = find_vagrantfile_dir()
    settings["repo_name"] = get_project_name_from_repo(settings.get("git_repo"), False)
    settings["project_name"] = get_project_name_from_repo(settings.get("git_repo"))
    settings_path = "".join(("./{0}/config/settings/{1}".format(settings.get("project_name"),
                                                                settings.get("abbrev_env")),
                             ".py"))
    settings["settings_path"] = ".".join(settings_path.split("/")[2:])
    settings["settings_path"] = ".".join(settings["settings_path"].split(".")[:-1])
    if settings["vault_used"] == "yes":
        secrets = {}
        for param in SECRETS_PARAMS:
            secrets[param] = settings[param]
        registered_settings = register_values_in_vault(vagrantfile_path,
                                                       "secret/{0}_{1}".format(settings["project_name"],
                                                                               settings["env"]),
                                                       secrets)
        for key in registered_settings:
            settings[key] = registered_settings[key]

    print("Current Settings:")
    pretty_print_dictionary(settings)
    raw_input("Press Enter to Continue or Ctrl+C to Cancel")
    local("cp -rf {0} ./templates.tmp".format(TEMPLATES_PATH))
    recursive_file_modify("./templates.tmp", settings)
    with lcd("./templates.tmp"):
        for filepath, dest_template in TEMPLATE_TO_PROJECT_MAPPING.iteritems():
            destination = dest_template.format(vagrantfile_path.rstrip('/'),
                                               settings.get("project_name"),
                                               settings.get("abbrev_env"),
                                               settings.get("env"))
            local("mv {0} {1}".format(filepath, destination))
    local("rm -rf ./templates.tmp")


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
        registered_settings = register_values_in_vault('.',
                                                       'secret/git_keys_{}'.format(generate_printable_string(25,
                                                                                                             False)),
                                                       {'public_key': public_key,
                                                        'private_key': private_key},
                                                       quoted=True
                                                       )
        settings['git_private_key'] = registered_settings['private_key']
        settings['git_public_key'] = registered_settings['public_key']

    if 'fabric_settings.py' in os.listdir('.'):
        continue_process = raw_input('You already have `fabric_settings.py` in this folder. Overwrite? (Y/N)')
        if continue_process.lower() == 'y':
            pass
        else:
            print("Aborted.")
            return False
    local('cp {0} ./fabric_settings.py'.format(os.path.join(FABFILE_PATH, "fabric_settings.py.default.py")))
    recursive_file_modify('./fabric_settings.py', settings, is_dir=False)
    print("".join(("You now have `fabric_settings.py`. Edit this file to have the correct ",
                   "values and then enter `yurt new_project`")))


@main.command()
@click.option("--dest", default=None, help='Vault file path destination. (Overrides defaults)')
def vault(dest):
    """
    Adds a vault that remote servers will push secrets to
    """
    settings = {}
    vault_UUID = ""
    protocol = ""
    for attribute, prompt in VAULT_ATTRIBUTES_TO_QUESTIONS.iteritems():
        response = raw_input(prompt)
        if attribute == "VAULT_UUID":
            if response == "":
                vault_UUID = generate_printable_string(20, False)
            else:
                vault_UUID = response
            continue
        if attribute == "PROTOCOL":
            protocol = "https://" if (response == "True") else "http://"
            continue
        if attribute == "VAULT_ADDR":
            response = "".join((protocol, response))
        settings[attribute] = response

    if dest:
        path_prefix = dest
    else:
        path_prefix = find_vagrantfile_dir()

    print("Vault Settings:")
    pretty_print_dictionary(settings)
    print("Vault_UUID: {0}".format(vault_UUID))
    dest_path = os.path.join(path_prefix, 'vault_{0}.json'.format(vault_UUID))
    print("Stored in {0}".format(dest_path))
    raw_input("Press Enter to Continue or Ctrl+C to Cancel")
    with open(dest_path, 'w') as outfile:
        json.dump(settings, outfile)

if __name__ == '__main__':
    main()
