# Zendesk Tickets Machine

[![CircleCI](https://circleci.com/gh/prontotools/zendesk-tickets-machine.svg?style=svg)](https://circleci.com/gh/prontotools/zendesk-tickets-machine)

## Docker Public Repository

https://hub.docker.com/r/prontotools/ztm-app/

## Installation
1. `touch .env`. This file keeps Zendesk configuration. If you don't want to connect to Zendesk, just keep this file empty.

#### Example configuration in `.env`:
```
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
```
2. `docker-compose up`