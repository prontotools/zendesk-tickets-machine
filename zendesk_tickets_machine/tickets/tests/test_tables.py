from django.conf import settings
from django.test import TestCase

from ..tables import TicketTable
from ..models import Ticket
from agents.models import Agent
from agent_groups.models import AgentGroup
from boards.models import Board

class TicketTableTest(TestCase):
    def test_ticket_table_should_have_all_defined_filed(self):
        agent = Agent.objects.create(
            name='Kan Ouivirach',
            zendesk_user_id='6969'
        )
        agent_group = AgentGroup.objects.create(name='Development')
        board = Board.objects.create(name='Pre-Production')

        comment = 'Thank you for signing up with us! ' \
            'Currently we are sorting out the info and will reach ' \
            'out again soon to continue with the setup.'

        ticket = Ticket()
        ticket.subject = 'Welcome to Pronto Service'
        ticket.comment = comment
        ticket.requester = 'client@hisotech.com'
        ticket.created_by = agent
        ticket.assignee = agent
        ticket.group = agent_group
        ticket.ticket_type = 'question'
        ticket.priority = 'urgent'
        ticket.tags = 'welcome'
        ticket.private_comment = 'Private comment'
        ticket.zendesk_ticket_id = '24328'
        ticket.board = board
        ticket.save()

        ticketTable = TicketTable(Ticket.objects.all())
        expected_fields = [
            '<input type="checkbox" name="select_all"/>',
            'Edit',
            'Delete',
            'Subject',
            'Comment',
            'Requester',
            'Created By',
            'Assignee',
            'Group',
            'Ticket Type',
            'Due Date',
            'Priority',
            'Tags',
            'Private Comment',
            'Zendesk Ticket Id'
        ]

        for each in expected_fields:
            self.assertTrue(each in ticketTable.as_values()[0])

        self.assertEqual(len(ticketTable.as_values()[0]), 15)

    def test_ticket_table_fields_should_show_dash_if_empty_and_set_default(self):
        agent = Agent.objects.create(
            name='Kan Ouivirach',
            zendesk_user_id='6969'
        )
        agent_group = AgentGroup.objects.create(name='Development')
        board = Board.objects.create(name='Pre-Production')

        comment = 'Thank you for signing up with us! ' \
            'Currently we are sorting out the info and will reach ' \
            'out again soon to continue with the setup.'

        ticket = Ticket()
        ticket.subject = 'Welcome to Pronto Service'
        ticket.comment = comment
        ticket.group = agent_group
        ticket.priority = 'urgent'
        ticket.private_comment = 'Private comment'
        ticket.zendesk_ticket_id = '24328'
        ticket.board = board
        ticket.save()

        ticketTable = TicketTable(Ticket.objects.all())

        expected_fields = [
            '<input type="checkbox" name="check" value="1"/>',
            'Edit',
            'Delete',
            'Welcome to Pronto Service',
            'Thank you for signing up with us! ' \
            'Currently we are sorting out the info and will ' \
            'reach out again soon to continue with the setup.',
            '-',
            '-',
            '-',
            agent_group,
            '-', 
            '-',
            'Urgent',
            '-',
            'Private comment',
            '24328'
        ]

        for each in expected_fields:
            self.assertTrue(each in ticketTable.as_values()[1])

        self.assertEqual(len(ticketTable.as_values()[1]), 15)

    def test_ticket_table_render_zendesk_zendesk_id_should_return_correctly(self):
        ticketTable = TicketTable({'test': 'test'})
        url = ticketTable.render_zendesk_ticket_id('1234')
        self.assertEqual(url, '<a href="%s/agent/tickets/1234" target="_blank">1234</a>' % settings.ZENDESK_URL)

