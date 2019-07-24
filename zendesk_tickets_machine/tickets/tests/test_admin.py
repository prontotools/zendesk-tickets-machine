from django.contrib.auth.models import User
from django.test import TestCase

from ..models import (
    Ticket,
    TicketZendeskAPIUsage
)
from agents.models import Agent
from agent_groups.models import AgentGroup
from boards.models import Board


class TicketAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.url = '/admin/tickets/ticket/'

    def test_access_ticket_admin_should_have_columns(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        board = Board.objects.create(name='Pre-Production')
        Ticket.objects.create(
            subject='Test Open Ticket',
            assignee=agent,
            group=agent_group,
            board=board
        )

        response = self.client.get(self.url)

        expected = '<div class="text"><a href="?o=1">Subject</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=2">Comment</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=3">Organization</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=4">Requester</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=5">Assignee</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=6">Ticket type</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=7">Due at</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=8">Priority</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=9">Tags</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=10">Cycle</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=11">Board</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=12">Is active</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

    def test_access_ticket_admin_should_have_board_filter(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        board = Board.objects.create(name='Pre-Production')
        Ticket.objects.create(
            subject='Test Open Ticket',
            assignee=agent,
            group=agent_group,
            board=board
        )

        response = self.client.get(self.url)

        expected = '<h3> By name </h3>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<h3> By is active </h3>'
        self.assertContains(response, expected, count=1, status_code=200)


class TicketZendeskAPIUsageAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.url = '/admin/tickets/ticketzendeskapiusage/'

    def test_access_ticket_api_usage_admin_should_have_columns(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        board = Board.objects.create(name='Pre-Production')
        TicketZendeskAPIUsage.objects.create(
            assignee=agent,
            ticket_type='question',
            priority='high',
            board=board
        )

        response = self.client.get(self.url)

        expected = '<div class="text"><a href="?o=1">Assignee</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=2">Organization</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=3">Requester</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=4">Ticket type</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=5">Priority</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=6">Board</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=7">Created</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

    def test_ticket_admin_should_have_export_button(self):
        response = self.client.get(self.url)

        expected = '<a href="' + self.url + 'export/?" ' \
            'class="export_link">Export</a>'
        self.assertContains(response, expected, count=1, status_code=200)


class TicketZendeskAPIUsageExportTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.url = '/admin/tickets/ticketzendeskapiusage/export/'

    def test_access_ticket_zendesk_api_usage_admin_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_ticket_zendesk_api_usage_admin_should_be_able_to_export_csv(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        board = Board.objects.create(name='Pre-Production')
        ticket_api_usage = TicketZendeskAPIUsage.objects.create(
            assignee=agent,
            ticket_type='question',
            priority='high',
            board=board
        )

        data = {
            'file_format': '0'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header('Content-Disposition'))
        self.assertEqual(response['Content-Type'], 'text/csv')

        expected = 'id,ticket_type,priority,assignee__name,board__name,created'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = f'{ticket_api_usage.id},question,high,Kan,Pre-Production'
        self.assertContains(response, expected, count=1, status_code=200)
