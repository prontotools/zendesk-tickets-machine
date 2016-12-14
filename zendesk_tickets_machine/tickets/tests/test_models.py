from django.test import TestCase

from ..models import Ticket
from agents.models import Agent
from agent_groups.models import AgentGroup


class TicketTest(TestCase):
    def test_save_ticket(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )

        comment = 'Thank you for signing up with us! ' \
            'Currently we are sorting out the info and will reach ' \
            'out again soon to continue with the setup.'

        ticket = Ticket()
        ticket.subject = 'Welcome to Pronto Service'
        ticket.comment = comment
        ticket.requester = 'client@hisotech.com'
        ticket.requester_id = '1095195473'
        ticket.assignee = agent
        ticket.group = agent_group
        ticket.ticket_type = 'question'
        ticket.priority = 'urgent'
        ticket.tags = 'welcome'
        ticket.private_comment = 'Private comment'
        ticket.zendesk_ticket_id = '24328'
        ticket.save()

        ticket = Ticket.objects.last()

        self.assertEqual(ticket.subject, 'Welcome to Pronto Service')
        self.assertEqual(ticket.comment, comment)
        self.assertEqual(ticket.requester, 'client@hisotech.com')
        self.assertEqual(ticket.requester_id, '1095195473')
        self.assertEqual(ticket.assignee.name, 'Kan')
        self.assertEqual(ticket.group.name, 'Development')
        self.assertEqual(ticket.ticket_type, 'question')
        self.assertEqual(ticket.priority, 'urgent')
        self.assertEqual(ticket.tags, 'welcome')
        self.assertEqual(ticket.private_comment, 'Private comment')
        self.assertEqual(ticket.zendesk_ticket_id, '24328')
