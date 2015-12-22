import os
import sys
from django.core.wsgi import get_wsgi_application

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

sys.path.append(os.path.abspath(os.path.join(PROJECT_ROOT, "../../")))

application = get_wsgi_application()
