from django.conf import settings

import requests


class Ticket(object):
    def __init__(self):
        self.zendesk_api_url = settings.ZENDESK_API_URL

    def create(self):
        url = self.zendesk_api_url+ '/api/v2/tickets.json'
        requests.post(url)
