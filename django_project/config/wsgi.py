import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%(project_name)s.%(development.settings_path)s")

application = get_wsgi_application()

