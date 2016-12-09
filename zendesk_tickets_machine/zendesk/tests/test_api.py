import os
from unittest.mock import patch

from django.test import TestCase

from ..api import Ticket


class TicketAPITest(TestCase):
    @patch('zendesk.api.requests.post')
    def test_create_ticket_on_zendesk_should_call_correct_url(self, mock):
        url = os.environ.get('ZENDESK_API_URL', '') + \
            '/api/v2/tickets.json'

        ticket = Ticket()
        ticket.create()

        mock.assert_called_once_with(url)
