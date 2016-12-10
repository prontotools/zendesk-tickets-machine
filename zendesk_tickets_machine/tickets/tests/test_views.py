from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import Ticket


class TicketViewTest(TestCase):
    def test_ticket_view_should_be_accessiable(self):
        response = self.client.get(reverse('tickets'))
        self.assertEqual(response.status_code, 200)

    def test_ticket_view_should_render_ticket_form(self):
        response = self.client.get(reverse('tickets'))

        expected = '<form method="post">'
        self.assertContains(response, expected, status_code=200)

        expected = "<input type='hidden' name='csrfmiddlewaretoken'"
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_subject" maxlength="300" name="subject" ' \
            'type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_comment" maxlength="500" name="comment" ' \
            'type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_requester" maxlength="100" ' \
            'name="requester" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_requester_id" maxlength="50" ' \
            'name="requester_id" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_assignee" maxlength="100" ' \
            'name="assignee" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_assignee_id" maxlength="50" ' \
            'name="assignee_id" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_ticket_type" maxlength="50" ' \
            'name="ticket_type" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_priority" maxlength="50" ' \
            'name="priority" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_tags" maxlength="300" name="tags" ' \
            'type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="submit">'
        self.assertContains(response, expected, status_code=200)

    def test_ticket_view_should_save_data_when_submit_form(self):
        data = {
            'subject': 'Welcome to Pronto Service',
            'comment': 'This is a comment.',
            'requester': 'client@hisotech.com',
            'requester_id': '1095195473',
            'assignee': 'kan@prontomarketing.com',
            'assignee_id': '1095195243',
            'ticket_type': 'question',
            'priority': 'urgent',
            'tags': 'welcome'
        }

        response = self.client.post(
            reverse('tickets'),
            data=data
        )

        ticket = Ticket.objects.last()

        self.assertEqual(ticket.subject, 'Welcome to Pronto Service')
        self.assertEqual(ticket.comment, 'This is a comment.')
        self.assertEqual(ticket.requester, 'client@hisotech.com')
        self.assertEqual(ticket.requester_id, '1095195473')
        self.assertEqual(ticket.assignee, 'kan@prontomarketing.com')
        self.assertEqual(ticket.assignee_id, '1095195243')
        self.assertEqual(ticket.ticket_type, 'question')
        self.assertEqual(ticket.priority, 'urgent')
        self.assertEqual(ticket.tags, 'welcome')

        expected = '<form method="post">'
        self.assertContains(response, expected, status_code=200)
