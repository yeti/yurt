# coding=utf-8
import click
from cookiecutter.main import cookiecutter

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
    print('==> Project created: {}'.format(result))
    print('==> To run dev project:')
    print('👉  cd {} && docker-compose up'.format(result))


if __name__ == '__main__':
    setup()
