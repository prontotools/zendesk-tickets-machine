from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from ..api import Ticket


class TicketAPITest(TestCase):
    def setUp(self):
        self.zendesk_api_url = settings.ZENDESK_API_URL

    @patch('zendesk.api.requests.post')
    def test_create_ticket_on_zendesk_should_call_correct_url(self, mock):
        url = self.zendesk_api_url + '/api/v2/tickets.json'

        ticket = Ticket()
        ticket.create()

        mock.assert_called_once_with(url)
