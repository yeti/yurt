import json
import os
from collections import OrderedDict
import click
from invoke import run
from invoke.exceptions import Failure
from yurt.yurt_core.utils import get_project_name_from_repo, generate_printable_string,\
                  recursive_file_modify, raw_input_wrapper, pretty_print_dictionary, \
                  find_vagrantfile_dir, register_values_in_vault, find_project_folder
from yurt.yurt_core.paths import TEMPLATES_PATH, YURT_PATH

TEMPLATE_FILES_TO_EXCLUDE_FROM_REMOTE_SERVER = ['yurtrc.template', 'temp_role', 'test_directory']

ATTRIBUTE_TO_QUESTION_MAPPING = OrderedDict([
    ("git_repo", "Enter the git repository link\n(i.e. git@github.com:mr_programmer/robot_repository.git):\t"),
    ("env", "What name is this environment (i.e. development, staging, production)?: "),
    ("abbrev_env", "How do you want this environment abbreviated (i.e. dev, stage, prod)?: "),
    ("app_host_dns", "What is the public DNS of this project's host (i.e. example.com)?: "),
    ("app_host_ip", "What is the IP of this project's host (i.e. 10.20.30.40)?: "),
    ("db_host_ip", "What is this project's DB host (Hint: same IP as before if hosted locally)?: "),
    ("debug", "This Django server will use Debug mode (True/False): "),
    ("num_gunicorn_workers", "".join(("How many gunicorn workers do you want ",
                                      "(Hint: For the number of workers, a go",
                                      "od rule to follow is 2 x number of CPUs + 1)?: "))),
    ("gunicorn_max_requests", "".join(("What do you want to set `gunicorn_max_requests` to ? ",
                                       "Setting this to 1 will restart the Gunicorn process each time ",
                                       "you make a request, basically reloading the code. Very han",
                                       "dy when developing. Set to 0 for unlimited requests.: "))),
    ("ssl_enabled", "Is SSL enabled on this server,\nor in other words, is it using 'https://' (yes/no)?: "),
    ("email_host", "Email host (default 'smtp.google.com')?: "),
    ("email_host_user", "Default email FROM user (i.e. 'dean@deanismyname.com' or optional)?: "),
    ("email_host_password", "Email user's password (optional)?: "),
    ("email_port", "Email server port (default 687): "),
    ("email_use_ssl", "Email server uses SSL (use `True` or `False`, default False)?: "),
    ("email_use_tls", "Email server uses TLS (use `True` or `False`, default True)?: "),
    ("git_branch", "From which git branch will the server pull the project?: "),
    ("vault_used", "Are you utilizing a vault to store secrets for this server (yes/no)?: "),
    ("multiple_yurt_project_server",
     "Does this server already have another Yurt-built project deployed on it (yes/no)?: ")
])

VAULT_ATTRIBUTES_TO_QUESTIONS = OrderedDict([
    ("PROTOCOL", "Is this vault ssl enabled (True/False)?: "),
    ("VAULT_ADDR", "What is the public IP/DNS of this vault (ex. example.com)?: "),
    ("VAULT_TOKEN", "What is your token for this vault?: "),
    ("VAULT_UUID", "What will you name this vault (leave blank for random)?: ")
])

TEMPLATE_TO_PROJECT_MAPPING = {
    "./templates.tmp/env_settings.py.template": "{0}/{1}/config/settings/{2}.py",
    "./templates.tmp/env_vars.yml.template": "{0}/{1}/orchestration/env_vars/{3}.yml",
    "./templates.tmp/inventory.template": "{0}/{1}/orchestration/inventory/{3}"
}

SECRETS_PARAMS = [
    "secret_key",
    "db_password",
    "email_host",
    "email_host_user",
    "email_host_password",
    "email_port",
]


@click.group()
def add():
    pass


@add.command()
@click.option("--git_repo", default=None, help="Git Repo Link to Yurt project")
@click.option("--env", default=None, help="Environment name (i.e. 'Development', 'Staging')")
@click.option("--abbrev_env", default=None, help="Abbreviated env name (i.e. 'dev', 'stage')")
@click.option("--app_host_ip", default=None, help="IP of App Server")
@click.option("--app_host_dns", default=None, help="DNS of App Server")
@click.option("--db_host_ip", default=None, help="IP of DB Server")
@click.option("--debug", default=None, help="Runs debug mode (use `True` or `False`)")
@click.option("--multiple_yurt_project_server", default=None, help="Server has other Yurt projects (use `yes` or `no`)")
@click.option("--num_gunicorn_workers", default=None, help="Number of Gunicorn workers")
@click.option("--gunicorn_max_requests", default=None, help="Number of Gunicorn max requests")
@click.option("--ssl_enabled", default=None, help="SSL is enabled on remote (use `yes` or `no`)")
@click.option("--git_branch", default=None, help="Git branch to pull from")
@click.option("--email_host", default=None, help="Email host DNS")
@click.option("--email_host_user", default=None, help="Default FROM email user")
@click.option("--email_host_password", default=None, help="FROM email user password")
@click.option("--email_port", default=None, help="Email server port (default 687)")
@click.option("--email_use_ssl", default=None, help="Email user uses SSL (use `True` or `False`, default False)?")
@click.option("--email_use_tls", default=None, help="Email user uses TLS (use `True` or `False`, default True)?")
@click.option("--vault_used", default=None, help="Uses 'vault_.json' file for vault lookup (use `yes` or `no`)")
def remote_server(**kwargs):
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
    raw_input_wrapper("You will be asked a bunch of questions for setting up the server.\nMake sure your "
                      "input is as accurate as possible.\nIf given a choice in parentheses, make sure\n"
                      "the input you enter matches one of those choices.\n"
                      "Press Enter to Continue.")

    # TODO: Abstract this question-loop with a re-usable util function
    try:
        question_items = ATTRIBUTE_TO_QUESTION_MAPPING.iteritems()
    except AttributeError:
        question_items = ATTRIBUTE_TO_QUESTION_MAPPING.items()

    for attribute, prompt in question_items:
        if kwargs[attribute] is None:
            settings[attribute] = raw_input_wrapper(prompt, attribute in lowercase_attrs)
            # Handle gunicorn defaults
            if attribute == "num_gunicorn_workers" and settings[attribute] == "":
                settings[attribute] = "2"
            if attribute == "gunicorn_max_requests" and settings[attribute] == "":
                settings[attribute] = "0"
            # Handle email defaults
            if attribute == "email_port" and settings[attribute] == "":
                settings[attribute] = "687"
            if attribute == "email_use_ssl" and settings[attribute] == "":
                settings[attribute] = "False"
            if attribute == "email_use_tls" and settings[attribute] == "":
                settings[attribute] = "True"
            # Handle other defaults
            if attribute == "multiple_yurt_project_server" and settings[attribute] == "":
                settings[attribute] = "no"
        else:
            settings[attribute] = kwargs[attribute]
    vagrantfile_path = find_vagrantfile_dir()
    settings["repo_name"] = get_project_name_from_repo(settings.get("git_repo"), False)
    settings["project_name"] = get_project_name_from_repo(settings.get("git_repo"))
    settings_path = "".join(("./{0}/config/settings/{1}".format(settings.get("project_name"),
                                                                settings.get("abbrev_env")),
                             ".py"))
    settings["settings_path"] = ".".join(settings_path.split("/")[2:])
    settings["settings_path"] = ".".join(settings["settings_path"].split(".")[:-1])
    if settings["vault_used"].lower() == "yes":
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
    raw_input_wrapper("Press Enter to Continue or Ctrl+C to Cancel")
    run("cp -rf {} ./templates.tmp".format(TEMPLATES_PATH))
    for excluded_file in TEMPLATE_FILES_TO_EXCLUDE_FROM_REMOTE_SERVER:
        run("rm -rf ./templates.tmp/{}".format(excluded_file))
    recursive_file_modify("./templates.tmp", settings)
    try:
        template_project_items = TEMPLATE_TO_PROJECT_MAPPING.iteritems()
    except AttributeError:
        template_project_items = TEMPLATE_TO_PROJECT_MAPPING.items()
    for file_path, dest_template in template_project_items:
        destination = dest_template.format(vagrantfile_path.rstrip('/'),
                                           settings.get("project_name"),
                                           settings.get("abbrev_env"),
                                           settings.get("env"))
        run("mv {} {}".format(file_path, destination))
    run("rm -rf ./templates.tmp")


@add.command()
@click.option("--dest", default=None, help='Vault file path destination. (Overrides defaults)')
def vault(dest):
    """
    Adds a vault config that remote servers can push secrets to
    """
    settings = {}
    vault_UUID = ""
    protocol = ""
    try:
        vault_items = VAULT_ATTRIBUTES_TO_QUESTIONS.iteritems()
    except AttributeError:
        vault_items = VAULT_ATTRIBUTES_TO_QUESTIONS.items()
    for attribute, prompt in vault_items:
        try:
            response = raw_input(prompt)
        except NameError:
            response = input(prompt)
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
    try:
        raw_input("Press Enter to Continue or Ctrl+C to Cancel")
    except NameError:
        input("Press Enter to Continue or Ctrl+C to Cancel")
    
    with open(dest_path, 'w') as outfile:
        json.dump(settings, outfile)


@add.command()
@click.option("--name",
              default=None,
              help='Ansible Role name')
@click.option("--remote/--local",
              default=False,
              help='Install role from Ansible Galaxy (remote) or generate one (local)')
def role(**kwargs):
    ROLE_ATTRIBUTE_MAPPING = OrderedDict([
        ('name', 'What will you name this role?: '),
        ('remote', 'Install existing role from Ansible Galaxy (Y/N)?: '),
    ])
    try:
        # Python 2
        question_items = ROLE_ATTRIBUTE_MAPPING.iteritems()
    except AttributeError:
        # Python 3
        question_items = ROLE_ATTRIBUTE_MAPPING.items()

    # TODO: Abstract this question-loop with a re-usable util function
    settings = {}
    for attribute, prompt in question_items:
        if kwargs[attribute] is None:
            settings[attribute] = raw_input_wrapper(prompt, True)
        else:
            settings[attribute] = kwargs[attribute]

    project_path = find_project_folder()
    path_to_roles = ['orchestration', 'roles']

    if settings['remote']:
        roles_path = os.path.join(project_path, *path_to_roles)
        ansible_galaxy_cmd = 'ansible-galaxy install -p {} {}'.format(roles_path, settings["name"])
    else:
        path_to_roles.append(settings['name'])
        roles_path = os.path.join(project_path, *path_to_roles)
        ansible_galaxy_cmd = 'ansible-galaxy init {} --force'.format(roles_path)
    try:
        run(ansible_galaxy_cmd)
    except Failure:
        if settings['remote']:
            raise ImportError('Role installation with Ansible Galaxy disabled on Python3.')
        else:
            print('WARN: Role-scaffolding with Ansible Galaxy disabled on Python3. Using custom scaffolding.')
            source_role_scaffold_path = os.path.join(YURT_PATH, 'templates', 'temp_role')
            ansible_galaxy_cmd = 'cp -rf {} {}'.format(source_role_scaffold_path, roles_path)
            run(ansible_galaxy_cmd)

if __name__ == '__main__':
    add()
