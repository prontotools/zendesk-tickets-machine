import os

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = INSTALLED_APPS + [
    'raven.contrib.django.raven_compat',
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

import dj_database_url
DATABASES['default'] =  dj_database_url.config()

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN')
}
