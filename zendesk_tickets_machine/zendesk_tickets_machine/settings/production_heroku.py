import os

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

import dj_database_url
DATABASES['default'] =  dj_database_url.config()

import raven
RAVEN_CONFIG = {
    'dsn': 'https://ac3ce45cbefe4db88cbb2afea2f5fc49:e76db4d607b54ba3bd238a9f7e171dd8@sentry.io/130625',
}
