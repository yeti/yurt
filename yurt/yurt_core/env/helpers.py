import os
from yurt.yurt_core.utils import Commands


class EnvCommand(Commands):

    subcommand = 'env'


# Helpers

def in_yurt_directory():
    return os.path.exists('./docker-compose.yml') and \
           os.path.exists('./django_app') and \
           os.path.exists('./envs')
