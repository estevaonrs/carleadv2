import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = os.getenv('DJANGO_DEBUG')

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

ROOT_URLCONF = 'fipe_project.urls'

WSGI_APPLICATION = 'fipe_project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
