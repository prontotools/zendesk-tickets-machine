#!/usr/bin/env bash

sleep 15

cd $APPLICATION_ROOT\zendesk_tickets_machine/
python manage.py migrate --settings=zendesk_tickets_machine.settings.production
python manage.py collectstatic --noinput --settings=zendesk_tickets_machine.settings.production
uwsgi --ini $APPLICATION_ROOT\ztm.ini
