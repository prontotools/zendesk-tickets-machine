import requests

from django.conf import settings


class Ticket(object):
    def __init__(self):
        self.zendesk_api_url = settings.ZENDESK_API_URL
        self.zendesk_api_user = settings.ZENDESK_API_USER
        self.zendesk_api_token = settings.ZENDESK_API_TOKEN
        self.headers = {'content-type': 'application/json'}

    def create(self, data):
        url = self.zendesk_api_url + '/api/v2/tickets.json'
        response = requests.post(
            url,
            auth=(self.zendesk_api_user, self.zendesk_api_token),
            headers=self.headers,
            json=data
        )
        return response.json()

    def create_comment(self, data, ticket_id):
        url = self.zendesk_api_url + f'/api/v2/tickets/{ticket_id}.json'
        response = requests.put(
            url,
            auth=(self.zendesk_api_user, self.zendesk_api_token),
            headers=self.headers,
            json=data
        )
        return response.json()


class User(object):
    def __init__(self):
        self.zendesk_api_url = settings.ZENDESK_API_URL
        self.zendesk_api_user = settings.ZENDESK_API_USER
        self.zendesk_api_token = settings.ZENDESK_API_TOKEN
        self.headers = {'content-type': 'application/json'}

    def search(self, query):
        url = self.zendesk_api_url + '/api/v2/users/search.json'
        payload = {
            'query': query
        }
        response = requests.get(
            url,
            auth=(self.zendesk_api_user, self.zendesk_api_token),
            headers=self.headers,
            params=payload
        )
        return response.json()


class Organization(object):
    def __init__(self):
        self.zendesk_api_url = settings.ZENDESK_API_URL
        self.zendesk_api_user = settings.ZENDESK_API_USER
        self.zendesk_api_token = settings.ZENDESK_API_TOKEN
        self.headers = {'content-type': 'application/json'}

    def show(self, organization_id):
        url = self.zendesk_api_url + \
            f'/api/v2/organizations/{organization_id}.json'
        response = requests.get(
            url,
            auth=(self.zendesk_api_user, self.zendesk_api_token),
            headers=self.headers,
        )
        return response.json()
