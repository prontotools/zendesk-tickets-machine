from django.test import TestCase

from ..models import (
    Ticket,
    TicketZendeskAPIUsage
)
from agents.models import Agent
from agent_groups.models import AgentGroup
from boards.models import Board


class TicketTest(TestCase):
    def test_save_ticket(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        board = Board.objects.create(
            name='Pre-Production',
            slug='pre-production'
        )

        comment = 'Thank you for signing up with us! ' \
            'Currently we are sorting out the info and will reach ' \
            'out again soon to continue with the setup.'

        ticket = Ticket()
        ticket.subject = 'Welcome to Pronto Service'
        ticket.comment = comment
        ticket.requester = 'client@hisotech.com'
        ticket.assignee = agent
        ticket.group = agent_group
        ticket.ticket_type = 'question'
        ticket.priority = 'urgent'
        ticket.tags = 'welcome'
        ticket.private_comment = 'Private comment'
        ticket.zendesk_ticket_id = '24328'
        ticket.board = board
        ticket.save()

        ticket = Ticket.objects.last()

        self.assertEqual(ticket.subject, 'Welcome to Pronto Service')
        self.assertEqual(ticket.comment, comment)
        self.assertEqual(ticket.requester, 'client@hisotech.com')
        self.assertEqual(ticket.assignee.name, 'Kan')
        self.assertEqual(ticket.group.name, 'Development')
        self.assertEqual(ticket.ticket_type, 'question')
        self.assertIsNone(ticket.due_at)
        self.assertEqual(ticket.priority, 'urgent')
        self.assertEqual(ticket.tags, 'welcome')
        self.assertEqual(ticket.private_comment, 'Private comment')
        self.assertEqual(ticket.zendesk_ticket_id, '24328')
        self.assertEqual(ticket.board.name, 'Pre-Production')
        self.assertTrue(ticket.is_active)

    def test_after_save_it_stores_usage_if_get_zendesk_ticket_id_first_time(
        self
    ):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        board = Board.objects.create(
            name='Pre-Production',
            slug='pre-production'
        )

        comment = 'Thank you for signing up with us! ' \
            'Currently we are sorting out the info and will reach ' \
            'out again soon to continue with the setup.'

        ticket = Ticket.objects.create(
            subject='Welcome to Pronto Service',
            comment=comment,
            requester='client@hisotech.com',
            assignee=agent,
            group=agent_group,
            ticket_type='question',
            priority='urgent',
            board=board
        )
        ticket.zendesk_ticket_id = '1234'
        ticket.save()

        usage = TicketZendeskAPIUsage.objects.last()

        self.assertEqual(usage.ticket_type, 'question')
        self.assertEqual(usage.priority, 'urgent')
        self.assertEqual(usage.assignee.name, 'Kan')
        self.assertEqual(usage.board.name, 'Pre-Production')
        self.assertTrue(usage.created)

    def test_after_save_it_should_not_store_usage_if_no_zendesk_ticket_id(
        self
    ):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        board = Board.objects.create(
            name='Pre-Production',
            slug='pre-production'
        )

        comment = 'Thank you for signing up with us! ' \
            'Currently we are sorting out the info and will reach ' \
            'out again soon to continue with the setup.'

        Ticket.objects.create(
            subject='Welcome to Pronto Service',
            comment=comment,
            requester='client@hisotech.com',
            assignee=agent,
            group=agent_group,
            ticket_type='question',
            priority='urgent',
            board=board
        )

        self.assertEqual(TicketZendeskAPIUsage.objects.count(), 0)


class TicketZendeskAPIUsageTest(TestCase):
    def test_save_ticket_zendesk_api_usage(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        board = Board.objects.create(
            name='Pre-Production',
            slug='pre-production'
        )

        usage = TicketZendeskAPIUsage()
        usage.ticket_type = 'question'
        usage.priority = 'normal'
        usage.assignee = agent
        usage.board = board
        usage.save()

        usage = TicketZendeskAPIUsage.objects.last()

        self.assertEqual(usage.ticket_type, 'question')
        self.assertEqual(usage.priority, 'normal')
        self.assertEqual(usage.assignee.name, 'Kan')
        self.assertEqual(usage.board.name, 'Pre-Production')
        self.assertTrue(usage.created)
