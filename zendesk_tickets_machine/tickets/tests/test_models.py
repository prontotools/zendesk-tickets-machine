from django.test import TestCase

from ..models import Ticket


class TicketTest(TestCase):
    def test_save_ticket(self):
        ticket = Ticket()
        ticket.subject = 'Welcome to Pronto Service'
        ticket.requester = 'client@hisotech.com'
        ticket.requester_id = '1095195473'
        ticket.assignee = 'kan@prontomarketing.com'
        ticket.assignee_id = '1095195243'
        ticket.ticket_type = 'question'
        ticket.priority = 'urgent'
        ticket.tags = 'welcome'
        ticket.save()

        ticket = Ticket.objects.last()

        self.assertEqual(ticket.subject, 'Welcome to Pronto Service')
        self.assertEqual(ticket.requester, 'client@hisotech.com')
        self.assertEqual(ticket.requester_id, '1095195473')
        self.assertEqual(ticket.assignee, 'kan@prontomarketing.com')
        self.assertEqual(ticket.assignee_id, '1095195243')
        self.assertEqual(ticket.ticket_type, 'question')
        self.assertEqual(ticket.priority, 'urgent')
        self.assertEqual(ticket.tags, 'welcome')
