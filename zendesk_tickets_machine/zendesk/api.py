import os
import requests


class Ticket(object):
    def create(self):
        zendesk_api_url = os.environ.get('ZENDESK_API_URL', '') + \
            '/api/v2/tickets.json'
        requests.post(zendesk_api_url)
