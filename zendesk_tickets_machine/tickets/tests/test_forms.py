from django.test import TestCase

from ..forms import TicketForm
from ..models import Ticket
from agents.models import Agent
from agent_groups.models import AgentGroup
from boards.models import Board


class TicketFormTest(TestCase):
    def test_ticket_form_should_have_all_defined_fields(self):
        form = TicketForm()

        expected_fields = [
            'subject',
            'comment',
            'requester',
            'requester_id',
            'assignee',
            'group',
            'ticket_type',
            'priority',
            'tags',
            'private_comment',
            'zendesk_ticket_id',
            'board',
        ]
        for each in expected_fields:
            self.assertTrue(each in form.fields)

        self.assertEqual(len(form.fields), 12)

    def test_ticket_form_should_save_zendesk_ticket_id_as_null(self):
        agent = Agent.objects.create(
            name='Kan Ouivirach',
            zendesk_user_id='6969'
        )
        agent_group = AgentGroup.objects.create(name='Development')
        board = Board.objects.create(name='Pre-Production')

        data = {
            'subject': 'Welcome',
            'comment': 'This is a comment.',
            'requester': 'customer@example.com',
            'requester_id': '12345',
            'assignee': agent.id,
            'group': agent_group.id,
            'ticket_type': 'task',
            'priority': 'urgent',
            'tags': 'welcome',
            'private_comment': 'Private comment',
            'board': board.id
        }
        form = TicketForm(data)
        form.save()

        ticket = Ticket.objects.last()
        self.assertIsNone(ticket.zendesk_ticket_id)
