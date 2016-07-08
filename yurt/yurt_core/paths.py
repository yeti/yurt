import os


YURT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DJANGO_PROJECT_PATH = os.path.join(YURT_PATH, 'django_project')
ORCHESTRATION_PROJECT_PATH = os.path.join(YURT_PATH, 'orchestration')
YURT_CORE_PATH = os.path.join(YURT_PATH, 'yurt_core')
TEMPLATES_PATH = os.path.join(YURT_PATH, "templates")
