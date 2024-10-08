from .environment import BASE_DIR
import os
from pathlib import Path
from dotenv import load_dotenv


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': 'root',
        'PASSWORD': os.getenv('MYSQL_ROOT_PASSWORD'),
        'HOST': 'db',
        'PORT': '3306',
    }
}

