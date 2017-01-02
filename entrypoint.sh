#!/usr/bin/env bash

cd $APPLICATION_ROOT\zendesk_tickets_machine/
#python manage.py migrate --settings=zendesk_tickets_machine.settings
python manage.py collectstatic --noinput --settings=zendesk_tickets_machine.settings
uwsgi --ini $APPLICATION_ROOT\ztm.ini
