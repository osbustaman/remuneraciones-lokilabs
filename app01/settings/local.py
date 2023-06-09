import os
from .base import *

from decouple import config

DEBUG = True

ALLOWED_HOSTS = ["*"]
PORT_LOCALHOST = '8080'
NAME_HOST = 'horus.desarollo'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('ENGINE'),
        'NAME': config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('HOST'),
        'PORT': config('PORT'),
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

WKHTMLTOPDF_BIN_PATH = '/usr/local/bin/wkhtmltopdf'

PDFKIT_CONFIG = {
    'wkhtmltopdf': '/usr/local/bin/wkhtmltopdf'
}
