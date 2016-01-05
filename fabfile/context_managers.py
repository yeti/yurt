from contextlib import contextmanager
from fabric.context_managers import prefix, cd


###
# Context Managers
###


@contextmanager
def bash():
    with prefix('source ~/.bashrc'):
        yield


@contextmanager
def venv(project_name):
    with bash():
        with prefix('workon %s' % project_name):
            yield


@contextmanager
def ansible():
    with bash():
        with prefix('workon ansible'):
            yield


@contextmanager
def in_project(project_name):
    with cd(project_name):
        yield
