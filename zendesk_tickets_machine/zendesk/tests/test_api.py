from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from ..api import Ticket, User


class TicketAPITest(TestCase):
    def setUp(self):
        self.zendesk_api_url = settings.ZENDESK_API_URL
        self.zendesk_api_user = settings.ZENDESK_API_USER
        self.zendesk_api_token = settings.ZENDESK_API_TOKEN
        self.headers = {'content-type': 'application/json'}

    @patch('zendesk.api.requests.post')
    def test_create_ticket_on_zendesk_should_send_data_to_zendesk_correctly(
        self,
        mock
    ):
        url = self.zendesk_api_url + '/api/v2/tickets.json'
        data = {
            'ticket': {
                'subject': 'My printer is on fire!',
                'requester_id': 1095195473,
                'assignee_id': 1095195243,
                'comment': {
                    'body': 'This is a comment'
                }
            }
        }

        ticket = Ticket()
        ticket.create(data)

        mock.assert_called_once_with(
            url,
            auth=(self.zendesk_api_user, self.zendesk_api_token),
            headers=self.headers,
            json=data
        )

    @patch('zendesk.api.requests.post')
    def test_create_ticket_on_zendesk_should_return_json(
        self,
        mock
    ):
        data = {}
        mock.return_value.json.return_value = {'key': 'value'}

        ticket = Ticket()
        result = ticket.create(data)

        self.assertEqual(result, {'key': 'value'})

    @patch('zendesk.api.requests.put')
    def test_create_comment_on_zendesk_should_send_data_to_zendesk_correctly(
        self,
        mock
    ):
        url = self.zendesk_api_url + '/api/v2/tickets/1.json'
        data = {
            'ticket': {
                'comment': {
                    'author_id': '123',
                    'body': 'Private comment',
                    'public': False
                }
            }
        }

        ticket = Ticket()
        ticket.create_comment(data, 1)

        mock.assert_called_once_with(
            url,
            auth=(self.zendesk_api_user, self.zendesk_api_token),
            headers=self.headers,
            json=data
        )

    @patch('zendesk.api.requests.put')
    def test_create_comment_on_zendesk_should_return_json(
        self,
        mock
    ):
        data = {}
        mock.return_value.json.return_value = {'key': 'value'}

        ticket = Ticket()
        result = ticket.create_comment(data, 1)

        self.assertEqual(result, {'key': 'value'})


class UserAPITest(TestCase):
    def setUp(self):
        self.zendesk_api_url = settings.ZENDESK_API_URL
        self.zendesk_api_user = settings.ZENDESK_API_USER
        self.zendesk_api_token = settings.ZENDESK_API_TOKEN
        self.headers = {'content-type': 'application/json'}

    @patch('zendesk.api.requests.get')
    def test_search_users_should_send_data_to_zendesk_correctly(self, mock):
        url = self.zendesk_api_url + '/api/v2/users/search.json'

        user = User()
        user.search('kan@prontomarketing.com')

        mock.assert_called_once_with(
            url + '?query=kan@prontomarketing.com',
            auth=(self.zendesk_api_user, self.zendesk_api_token),
            headers=self.headers
        )

    @patch('zendesk.api.requests.get')
    def test_search_users_should_return_json(self, mock):
        mock.return_value.json.return_value = {'key': 'value'}

        user = User()
        result = user.search('kan@prontomarketing.com')

        self.assertEqual(result, {'key': 'value'})
