# coding=utf-8

import os
import re
from shutil import copy2, make_archive
from zipfile import ZipFile

import click
import yaml
from cookiecutter.main import cookiecutter

from yurt.yurt_core.utils import get_iter


def add():
    # Create env var file in envs
    os.chdir('./envs')
    result_path = cookiecutter('gh:yeti/yurt_template-envvars')
    environment = re.search(r'envs/(.+)\.env\.d$', result_path).group(1)

    # Copy docker-compose.remote.yml
    os.chdir('..')
    target_file = './docker-compose.{}.yml'.format(environment)
    copy2(
        './docker-compose.remote.yml',
        './docker-compose.{}.yml'.format(environment)
    )

    # Edit copy with new env vars
    with open(target_file, 'r+') as target_file_obj:
        compose_contents = yaml.load(target_file_obj.read())
        target_file_obj.seek(0)
        target_file_obj.truncate()
        env_file = './envs/{}.env'.format(environment)

        all_services = compose_contents.get('services', {})
        for key, _ in get_iter(all_services):
            all_services[key]['env_file'] = [env_file]
        compose_contents['services'] = all_services
        yaml.dump(compose_contents, target_file_obj, default_flow_style=False)

    click.echo('==> Environment variable files added to project')
    click.echo('==> Deploy the project accordingly:')
    click.echo('==> 👉 eval `docker-machine env <remote_machine>`')
    click.echo('==> 👉 docker-compose -f docker-compose.{}.yml up'.format(environment))


def import_func(src):
    click.echo('==> Extracting {} into ./envs'.format(src))
    with ZipFile(src) as zip_stream:
        zip_stream.extractall('./envs')
    click.echo('==> Success!')


def export(filename):
    click.echo('==> Exporting .envs/ into ./{}.zip'.format(filename))
    make_archive(filename, 'zip', './envs')
    click.echo('==> Success!')
    click.echo('==> Upload this zip archive to a vault. To import:')
    click.echo('👉  yurt env import <path-to-archive>')

