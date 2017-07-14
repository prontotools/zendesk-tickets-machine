#!/usr/bin/env bash

sleep 5

cd $APPLICATION_ROOT\zendesk_tickets_machine/
python manage.py migrate --settings=zendesk_tickets_machine.settings.local
python manage.py runserver 0.0.0.0:8000 --settings=zendesk_tickets_machine.settings.local
