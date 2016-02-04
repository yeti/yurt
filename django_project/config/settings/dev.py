from .base import *

DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "%(development.secret_key)s"

ALLOWED_HOSTS = ['%(development.app_host_ip)s']
