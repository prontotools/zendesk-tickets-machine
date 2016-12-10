from django.conf import settings

import requests


class Ticket(object):
    def __init__(self):
        self.zendesk_api_url = settings.ZENDESK_API_URL
        self.zendesk_api_user = settings.ZENDESK_API_USER
        self.zendesk_api_token = settings.ZENDESK_API_TOKEN
        self.headers = {'content-type': 'application/json'}

    def create(self, data):
        url = self.zendesk_api_url+ '/api/v2/tickets.json'
        response = requests.post(
            url,
            auth=(self.zendesk_api_user, self.zendesk_api_token),
            headers=self.headers,
            json=data
        )
        return response.json()
