# flake8: Noqa
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')

DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS: list[str] = []

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',    'PAGE_SIZE': 10
}
