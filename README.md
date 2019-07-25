# Zendesk Tickets Machine

[![CircleCI](https://circleci.com/gh/prontotools/zendesk-tickets-machine.svg?style=svg)](https://circleci.com/gh/prontotools/zendesk-tickets-machine)
[![BCH compliance](https://bettercodehub.com/edge/badge/prontotools/zendesk-tickets-machine?branch=develop)](https://bettercodehub.com/)

Machine that helps us fire Zendesk tickets using our defined ticket templates

## Development Setup

Mac OS or Linux:

```sh
touch .env
```

This `.env` file keeps the configuration. This file can be left empty like this.

```sh
ZENDESK_URL=xxx
ZENDESK_API_URL=xxx
ZENDESK_API_USER=xxx
ZENDESK_API_TOKEN=xxx
SENTRY_DSN=xxx
FIREBASE_API_KEY=xxx
FIREBASE_AUTH_DOMAIN=xxx
FIREBASE_DATABASE_URL=xxx
FIREBASE_PROJECT_ID=xxx
FIREBASE_STORAGE_BUCKET=xxx
FIREBASE_MESSAGING_SENDER_ID=xxx
DEFAULT_ZENDESK_USER_ID=xxx
```

To start the app, run:

```sh
docker-compose up --build
```

To create a superuser, run:
```sh
docker exec -it zendeskticketsmachine_app_1 bash
cd zendesk_tickets_machine
python manage.py createsuperuser
```

The app will run at http://localhost:8090/.
