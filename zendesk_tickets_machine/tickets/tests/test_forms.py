import datetime

from django.test import TestCase

from ..forms import TicketForm, TicketUpdateOnceForm
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
            'created_by',
            'assignee',
            'group',
            'ticket_type',
            'due_at',
            'priority',
            'tags',
            'private_comment',
            'zendesk_ticket_id',
            'board',
        ]
        for each in expected_fields:
            self.assertTrue(each in form.fields)

        self.assertEqual(len(form.fields), 13)

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
            'created_by': agent.id,
            'assignee': agent.id,
            'group': agent_group.id,
            'ticket_type': 'task',
            'due_at': datetime.datetime(2017, 1, 1, 12, 30, 59, 0),
            'priority': 'urgent',
            'tags': 'welcome',
            'private_comment': 'Private comment',
            'board': board.id
        }
        form = TicketForm(data)
        form.save()

        ticket = Ticket.objects.last()
        self.assertIsNone(ticket.zendesk_ticket_id)

    def test_ticket_form_should_save_tags_as_empty(self):
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
            'created_by': agent.id,
            'assignee': agent.id,
            'group': agent_group.id,
            'ticket_type': 'task',
            'due_at': datetime.datetime(2017, 1, 1, 12, 30, 59, 0),
            'priority': 'urgent',
            'tags': None,
            'private_comment': 'Private comment',
            'board': board.id
        }
        form = TicketForm(data)
        form.save()

        ticket = Ticket.objects.last()
        self.assertEqual(ticket.tags, '')

    def test_ticket_form_should_have_defined_attributes(self):
        form = TicketForm()
        self.assertEqual(
            form.fields['ticket_type'].widget.attrs,
            {
                'class': 'form-control',
                'onChange': 'check_ticket_type()'
            }
        )
        self.assertEqual(
            form.fields['due_at'].widget.attrs,
            {
                'class': 'form-control',
                'id': 'datepicker',
                'size': '10'}
        )


class TicketUpdateOnceFormTest(TestCase):
    def test_ticket_update_once_form_should_have_all_defined_fields(self):
        form = TicketUpdateOnceForm()

        expected_fields = [
            'subject',
            'requester',
            'tags',
            'due_at',
            'assignee',
        ]
        for each in expected_fields:
            self.assertTrue(each in form.fields)

        self.assertEqual(len(form.fields), 5)

    def test_ticket_update_once_form_should_have_defined_attributes(self):
        form = TicketUpdateOnceForm()
        self.assertEqual(
            form.fields['subject'].widget.attrs,
            {'id': 'edit_subject'}
        )
        self.assertEqual(
            form.fields['requester'].widget.attrs,
            {'id': 'edit_requester'}
        )
        self.assertEqual(
            form.fields['tags'].widget.attrs,
            {'id': 'edit_tags'}
        )
        self.assertEqual(
            form.fields['due_at'].widget.attrs,
            {
                'class': 'datepicker',
                'id': 'edit_due_at',
                'size': '10'
            }
        )
        self.assertEqual(
            form.fields['assignee'].widget.attrs,
            {'id': 'edit_assignee'}
        )
