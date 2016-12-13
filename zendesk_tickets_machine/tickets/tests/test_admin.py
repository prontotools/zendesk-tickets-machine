from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Ticket
from agents.models import Agent


class TicketAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.url = '/admin/tickets/ticket/'

    def test_access_ticket_admin_should_have_columns(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        Ticket.objects.create(
            subject='Test Open Ticket',
            assignee=agent
        )

        response = self.client.get(self.url)

        expected = '<div class="text"><a href="?o=1">Subject</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=2">Comment</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=3">Requester</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=4">Requester id</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=5">Assignee</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=6">Ticket type</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=7">Priority</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=8">Tags</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)
