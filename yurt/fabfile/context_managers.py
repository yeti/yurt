from contextlib import contextmanager
from fabric.context_managers import prefix, cd, lcd
import os

###
# Context Managers
###


@contextmanager
def bash():
    if os.path.exists(os.path.expanduser("~/.bashrc")):
        with prefix('source ~/.bashrc'):
            yield
    else:
        with prefix('source ~/.bash_profile'):
            yield


@contextmanager
def venv(project_name):
    with bash():
        with prefix('workon {}'.format(project_name)):
            yield


@contextmanager
def in_project(project_name):
    with lcd(project_name):
        yield
