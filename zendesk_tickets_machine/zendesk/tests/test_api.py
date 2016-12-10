from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from ..api import Ticket


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
