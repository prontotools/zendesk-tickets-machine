"""
WSGI config for zendesk_tickets_machine project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zendesk_tickets_machine.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
application = Sentry(application)
