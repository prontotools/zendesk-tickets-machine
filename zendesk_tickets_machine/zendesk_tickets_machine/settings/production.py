from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = INSTALLED_APPS + [
    'raven.contrib.django.raven_compat',
]

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN')
}

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ztm',
        'USER': 'ztm',
        'PASSWORD': os.environ.get('ZTM_DATABASE_PASSWORD', ''),
        'HOST': 'db',
        'PORT': '5432',
    }
}

########## VISUALLY DISTINGUISH ENVIRONMENTS

ENVIRONMENT_NAME = 'production'
ENVIRONMENT_COLOR = '#ff2222'

########## END VISUALLY DISTINGUISH ENVIRONMENTS