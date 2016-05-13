import json
import os
from collections import OrderedDict

import hvac
from fabric.decorators import task
from fabric.operations import local
from fabric.context_managers import lcd
from fabric.operations import local

from cli import main
from setup import YURT_PATH

TEMPLATES_PATH = os.path.join(YURT_PATH, "templates")
from utils import get_project_name_from_repo, generate_printable_string,\
                  recursive_file_modify, raw_input_wrapper, pretty_print_dictionary, \
                  get_vault_credentials_from_path

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
    "./env_settings.py.template.py": "../{0}/config/settings/{1}.py",
    "./env_vars.yml.template": "../{0}/orchestration/env_vars/{2}.yml",
    "./inventory.template": "../{0}/orchestration/inventory/{2}"
}

SECRETS_PARAMS = [
    "secret_key",
    "db_password"
]

@main.command()
def remote_server():
    """
    Adds remote server files for deploying to new remote servers
    :return:
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
    settings["repo_name"] = get_project_name_from_repo(settings.get("git_repo"), False)
    settings["project_name"] = get_project_name_from_repo(settings.get("git_repo"))
    settings_path = "".join(("./{0}/config/settings/{1}".format(settings.get("project_name"),
                                                                settings.get("abbrev_env")),
                             ".py"))
    settings["settings_path"] = ".".join(settings_path.split("/")[2:])
    settings["settings_path"] = ".".join(settings["settings_path"].split(".")[:-1])
    if settings["vault_used"] == "yes":
        vault_address, vault_token, vault_path = get_vault_credentials_from_path(".")

        vault_client = hvac.Client(url=vault_address, token=vault_token)
        if vault_client.is_authenticated() and not vault_client.is_sealed():
            secrets = {}
            vault_secret_path = "secret/{0}_{1}".format(settings["project_name"],
                                                        settings["env"])
            for param in SECRETS_PARAMS:
                secrets[param] = settings[param]
                settings[param] = " ".join(("{{",
                                            "lookup('vault', '{0}', '{1}', '{2}')".format(vault_secret_path,
                                                                                          param,
                                                                                          vault_path),
                                            "}}"))
            vault_client.write(vault_secret_path, **secrets)
        else:
            raise Exception("Vault connection is down.")

    print("Current Settings:")
    pretty_print_dictionary(settings)
    raw_input("Press Enter to Continue or Ctrl+C to Cancel")
    local("cp -rf {0} ./templates.tmp".format(TEMPLATES_PATH))
    recursive_file_modify("./templates.tmp", settings)
    with lcd("./templates.tmp"):
        for filepath, dest_template in TEMPLATE_TO_PROJECT_MAPPING.iteritems():
            destination = dest_template.format(settings.get("project_name"),
                                               settings.get("abbrev_env"),
                                               settings.get("env"))
            local("mv {0} {1}".format(filepath, destination))
    local("rm -rf ./templates.tmp")


@main.command()
def vault():
    """
    Adds a vault that remote servers will push to
    :return:
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
    print("Vault Settings:")
    pretty_print_dictionary(settings)
    print("Vault_UUID: {0}".format(vault_UUID))
    raw_input("Press Enter to Continue or Ctrl+C to Cancel")
    if os.path.exists("./Vagrantfile"):
        path_prefix = "./"
    else:
        path_prefix = "../"
    with open(os.path.join(path_prefix, 'vault_{0}.json'.format(vault_UUID)), 'w') as outfile:
        json.dump(settings, outfile)
