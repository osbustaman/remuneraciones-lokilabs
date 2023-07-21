import os
from .base import *

from decouple import config

DEBUG = True

ALLOWED_HOSTS = ["*"]
if config('WORK_ENVIRONMENT') == "local":
    PORT_LOCALHOST = config('PORT_LOCALHOST')
else:
    PORT_LOCALHOST = ""
NAME_HOST = config('NAME_HOST')

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
MEDIA_URL = '/media/'
MEDIA_ROOT = ''.join(os.path.join(BASE_DIR, 'media'))

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

WKHTMLTOPDF_BIN_PATH = '/usr/local/bin/wkhtmltopdf'

PDFKIT_CONFIG = {
    'wkhtmltopdf': '/usr/local/bin/wkhtmltopdf'
}

CORS_REPLACE_HTTPS_REFERER      = False
HOST_SCHEME                     = "http://"
SECURE_PROXY_SSL_HEADER         = None
SECURE_SSL_REDIRECT             = False
SESSION_COOKIE_SECURE           = False
CSRF_COOKIE_SECURE              = False
SECURE_HSTS_SECONDS             = None
SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
SECURE_FRAME_DENY               = False
