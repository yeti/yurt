from .base import *

DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "%(vagrant.secret_key)s"

ALLOWED_HOSTS = ['*']