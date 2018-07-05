import click
import os
import yaml
from invoke import run
from yurt.yurt_core.utils import raw_input_wrapper, recursive_file_modify, find_project_folder,\
    get_project_name_from_repo, get_owner_name_from_repo, generate_options
from yurt.yurt_core.paths import TEMPLATES_PATH, YURTRC_PATH
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

__author__ = 'deanmercado'


@click.group()
@click.pass_context
def deploy_cli(ctx):
    pass


# TODO: make a more flexible engine for editing/reading from .yurtrc
def create_yurtrc_with_access_token():
    print(
        '\n'.join([
            'You will need to setup an access token for your Github user account.',
            'To do so:',
            '1) Go to github.com and log-in',
            '2) In the top right, click on your user image and go to \'Settings\' in the dropdown',
            '3) Under \'Developer Settings\' on the left side-bar, click on \'Personal access tokens\'.',
            '4) Click on the \'Generate new token\' button.',
            '5) Make sure this token has ALL the permissions.'
        ])
    )
    github_access_key = raw_input_wrapper('\n'.join((
       '6) Once your token has been generated, copy-paste it below and hit Enter.',
       'Access Token: ')))
    yurtrc_path = os.path.join(TEMPLATES_PATH, 'yurtrc.template')
    template_vars = {'github_access_key': github_access_key}
    run('cp {} {}'.format(yurtrc_path, YURTRC_PATH))
    recursive_file_modify(YURTRC_PATH, template_vars, is_dir=False)


def output_git_user_access_key():
    cfg_parser = ConfigParser()
    with open(os.path.expanduser('~/.yurtrc'), 'r') as yurtrc_file:
        cfg_parser.readfp(yurtrc_file)
        github_access_token = cfg_parser.get('Yurt', 'github_access_key')
    return github_access_token


def output_var_from_base_yml(variable):
    project_dir = find_project_folder()
    if project_dir:
        base_vars_path = os.path.join(project_dir, 'orchestration', 'env_vars', 'base.yml')
        with open(base_vars_path, 'r') as base_yaml_file:
            base_yaml = yaml.load(base_yaml_file.read())
            target_value = base_yaml.get(variable, None)
        return target_value
    else:
        raise OSError('Not in a Yurt project folder')


def run_playbook(selection, first_time_setup):
    if first_time_setup == 'n':
        deploy_tag = '--tags "deploy"'
    else:
        deploy_tag = ''
    run('ansible-playbook {} -i orchestration/inventory/{} orchestration/site.yml'.format(deploy_tag, selection))


@deploy_cli.command()
@click.option('--selection', default=None, help='Name of the inventory to deploy with ansible-playbook')
@click.pass_context
def deploy(ctx, selection):
    """
    Starts deploy process
    """
    if not os.path.exists("orchestration"):
        project_path = find_project_folder()
        if project_path:
            os.chdir(project_path)
        else:
            raise OSError('Not in a Yurt project folder')

    if selection is None:
        options_string, options = generate_options(
            os.listdir("./orchestration/inventory"),
            item_label="Inventory",
            exclude=["vagrant"]
        )
        print(options_string)
        num_selection = raw_input_wrapper("Which environment do you want to deploy (use Option number)?:\t")
        selection = options[num_selection]

    # Check if user has added deploy keys for the git repo
    not_first_timer = raw_input_wrapper("Have you added deploy keys for this git repo yet (y/n)?: ", True)
    first_time_setup = raw_input_wrapper("Is this project being set up from scratch(y), or are you deploying to existing(n)?: ", True)

    if not_first_timer in ['n', 'y']:
        if not_first_timer == 'n':
            if not os.path.exists(YURTRC_PATH):
                # Create the access_key/yurtrc file
                create_yurtrc_with_access_token()
            # Use the access_key in ~/.yurtrc to POST git ssh pub key to server
            access_key = output_git_user_access_key()
            # Get needed variables from base_yml
            git_ssh_pub_key = output_var_from_base_yml('git_ssh_pub_key')
            git_repo = output_var_from_base_yml('git_repo')
            project_name = get_project_name_from_repo(git_repo, drop_hyphens=False)
            owner_name = get_owner_name_from_repo(git_repo)
            compiled_curl_command = ' '.join((
                'curl -X POST',
                '-H "Content-Type:application/json"',
                '-d \'{{"title": "{}@{}", "key": "{}"}}\''.format(project_name, selection, git_ssh_pub_key),
                'https://api.github.com/repos/{}/{}/keys?access_token={}'.format(owner_name, project_name, access_key))),
            run(compiled_curl_command)
        run_playbook(selection, first_time_setup)

    else:
        print('Bad input! Try again.')
        ctx.invoke(deploy, selection=selection)

if __name__ == '__main__':
    deploy_cli()
