import os
import re
from collections import OrderedDict

from fabric.decorators import task
from fabric.operations import local
from fabric.context_managers import lcd
from context_managers import bash

from utils import add_fab_path_to_bashrc, get_project_name_from_repo, \
    generate_printable_string, recursive_file_modify, raw_input_wrapper

ATTRIBUTE_TO_QUESTION_MAPPING = OrderedDict([
    ("git_repo", "Enter the git repository link\n(i.e. git@github.com:mr_programmer/robot_repository.git):\t"),
    ("env", "What name is this environment (ie development, staging, production)?:\t "),
    ("abbrev_env", "How do you want this environment abbreviated (i.e. dev, stage, prod)?:\t "),
    ("app_host_ip", "What is the public IP address of this project's host (i.e. 123.45.67.89)?:\t"),
    ("db_host_ip", "What is the IP address of this project's DB host (Hint: `app_host_ip` if hosted locally)?:\t"),
    ("debug", "This Django server will use Debug mode (True/False):\t"),
    ("num_gunicorn_workers", "".join(("How many gunicorn workers do you want ",
                                      "(Hint: For the number of workers, a go",
                                      "od rule to follow is 2 x number of CPUs + 1)?:\t"))),
    ("gunicorn_max_requests", "".join(("What do you want to set `gunicorn_max_requests` to ? ",
                                       "Setting this to 1 will restart the Gunicorn process each time ",
                                       "you make a request, basically reloading the code. Very han",
                                       "dy when developing. Set to 0 for unlimited requests.:\t"))),
    ("ssl_enabled", "Is SSL enabled on this server (yes/no)?:\t"),
    ("git_branch", "From which git branch will the server pull the project?:\t")
])

TEMPLATE_TO_PROJECT_MAPPING = {
    "./env_settings.py.template.py": "../{0}/config/settings/{1}.py",
    "./env_vars.yml.template": "../{0}/orchestration/env_vars/{2}.yml",
    "./inventory.template": "../{0}/orchestration/inventory/{2}"
}


@task
def remote_server():
    if os.path.exists("./templates.tmp"):
        print "A `templates.tmp` directory is in the current working directory. Delete this before trying again."
        return None
    add_fab_path_to_bashrc()
    lowercase_attrs = ["env", "abbrev_env"]
    settings = {
        "secret_key": generate_printable_string(40),
        "db_password": generate_printable_string(20, False),
    }
    raw_input("You will be asked a bunch of questions for setting up the server.\nMake sure your "
              "input is as accurate as possible.\nIf given a choice in parentheses, make sure\n"
              "the choice you enter matches one of those choices.\n"
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

    print "Current Settings: \n{"
    for attr, value in settings.iteritems():
        print "{0} : {1}, ".format(attr, value)
    print "}\n"
    raw_input("Press Enter to Continue or Ctrl+C to Cancel")
    with bash():
        local("cp -rf $FAB_PATH/../templates ./templates.tmp")
        recursive_file_modify("./templates.tmp", settings)
    with lcd("./templates.tmp"):
        for filepath, dest_template in TEMPLATE_TO_PROJECT_MAPPING.iteritems():
            destination = dest_template.format(settings.get("project_name"),
                                               settings.get("abbrev_env"),
                                               settings.get("env"))
            local("mv {0} {1}".format(filepath, destination))
    local("rm -rf ./templates.tmp")
