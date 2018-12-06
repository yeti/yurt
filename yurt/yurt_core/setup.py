# coding=utf-8
import click
from cookiecutter.main import cookiecutter

from yurt.yurt_core.utils import echo_multiline

__author__ = 'deanmercado'


@click.group()
def setup():
    pass


@setup.command()
def new():
    """
    Create new project
    """
    template_location = 'gh:yeti/yurt_template-django'
    print('==> Creating a new project with Yurt Django 2.0 Template')
    result = cookiecutter(template_location)
    echo_multiline("""
==> Yurt project created:
{result}

==> Run dev project:
cd {result} && docker-compose up

""".format(result=result))
