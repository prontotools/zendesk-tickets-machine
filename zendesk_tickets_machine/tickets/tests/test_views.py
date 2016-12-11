import json
from unittest.mock import patch

from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import Ticket


class TicketViewTest(TestCase):
    def test_ticket_view_should_be_accessible(self):
        response = self.client.get(reverse('tickets'))
        self.assertEqual(response.status_code, 200)

    def test_ticket_view_should_have_table_header(self):
        response = self.client.get(reverse('tickets'))

        expected = '<th>Subject</th>' \
            '<th>Comment</th>' \
            '<th>Requester</th>' \
            '<th>Requester ID</th>' \
            '<th>Assignee</th>' \
            '<th>Assignee ID</th>' \
            '<th>Group</th>' \
            '<th>Ticket Type</th>' \
            '<th>Priority</th>' \
            '<th>Tags</th>' \
            '<th>Status</th>' \
            '<th>Private Comment</th>' \
            '<th>Zendesk Ticket ID</th>' \
            '<th>Stage</th>' \
            '<th>Vertical</th>'
        self.assertContains(response, expected, count=2, status_code=200)

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

        expected = '<input id="id_group" maxlength="50" ' \
            'name="group" type="text" required />'
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

        expected = '<input id="id_status" maxlength="300" name="status" ' \
            'type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_private_comment" maxlength="500" ' \
            'name="private_comment" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_zendesk_ticket_id" maxlength="50" ' \
            'name="zendesk_ticket_id" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_stage" maxlength="10" name="stage" ' \
            'type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_vertical" maxlength="30" name="vertical" ' \
            'type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="submit">'
        self.assertContains(response, expected, status_code=200)

    def test_ticket_view_should_show_ticket_list(self):
        Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            requester_id='1095195473',
            assignee='kan@prontomarketing.com',
            assignee_id='1095195243',
            group='Marketing Services',
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            status='open',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            stage='A',
            vertical='NASS'
        )
        Ticket.objects.create(
            subject='Ticket 2',
            comment='Comment 2',
            requester='client+another@hisotech.com',
            requester_id='1095195474',
            assignee='kan+another@prontomarketing.com',
            assignee_id='1095195244',
            group='Marketing Services',
            ticket_type='question',
            priority='high',
            tags='welcome internal',
            status='open',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            stage='A',
            vertical='NASS'
        )

        response = self.client.get(reverse('tickets'))

        expected = '<tr><td>Ticket 1</td><td>Comment 1</td>' \
            '<td>client@hisotech.com</td><td>1095195473</td>' \
            '<td>kan@prontomarketing.com</td><td>1095195243</td>' \
            '<td>Marketing Services</td><td>question</td><td>urgent</td>' \
            '<td>welcome</td><td>open</td><td>Private comment</td>' \
            '<td>24328</td><td>A</td><td>NASS</td></tr>'
        self.assertContains(response, expected, status_code=200)

        expected = '<tr><td>Ticket 2</td><td>Comment 2</td>' \
            '<td>client+another@hisotech.com</td><td>1095195474</td>' \
            '<td>kan+another@prontomarketing.com</td><td>1095195244</td>' \
            '<td>Marketing Services</td><td>question</td><td>high</td>' \
            '<td>welcome internal</td><td>open</td>' \
            '<td>Private comment</td><td>24328</td><td>A</td>' \
            '<td>NASS</td></tr>'
        self.assertContains(response, expected, status_code=200)

    def test_ticket_view_should_save_data_when_submit_form(self):
        data = {
            'subject': 'Welcome to Pronto Service',
            'comment': 'This is a comment.',
            'requester': 'client@hisotech.com',
            'requester_id': '1095195473',
            'assignee': 'kan@prontomarketing.com',
            'assignee_id': '1095195243',
            'group': 'Marketing Services',
            'ticket_type': 'question',
            'priority': 'urgent',
            'tags': 'welcome',
            'status': 'open',
            'private_comment': 'Private comment',
            'zendesk_ticket_id': '24328',
            'stage': 'A',
            'vertical': 'NASS'
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
        self.assertEqual(ticket.group, 'Marketing Services')
        self.assertEqual(ticket.ticket_type, 'question')
        self.assertEqual(ticket.priority, 'urgent')
        self.assertEqual(ticket.tags, 'welcome')
        self.assertEqual(ticket.status, 'open')
        self.assertEqual(ticket.private_comment, 'Private comment')
        self.assertEqual(ticket.zendesk_ticket_id, '24328')
        self.assertEqual(ticket.stage, 'A')
        self.assertEqual(ticket.vertical, 'NASS')

        expected = '<form method="post">'
        self.assertContains(response, expected, status_code=200)

        expected = '<tr><td>Welcome to Pronto Service</td>' \
            '<td>This is a comment.</td><td>client@hisotech.com</td>' \
            '<td>1095195473</td><td>kan@prontomarketing.com</td>' \
            '<td>1095195243</td><td>Marketing Services</td>' \
            '<td>question</td><td>urgent</td><td>welcome</td>' \
            '<td>open</td><td>Private comment</td><td>24328</td>' \
            '<td>A</td><td>NASS</td></tr>'
        self.assertContains(response, expected, status_code=200)


class TicketNewViewTest(TestCase):
    @patch('tickets.views.ZendeskTicket')
    def test_ticket_new_view_should_be_accessible(self, mock):
        mock.return_value.create.return_value = {}

        response = self.client.get(
            reverse('tickets_new', kwargs={'ticket_id': 1})
        )

        self.assertEqual(response.status_code, 200)

    @patch('tickets.views.ZendeskTicket')
    def test_ticket_new_view_should_send_data_to_create_zendesk_ticket(
        self,
        mock
    ):
        mock.return_value.create.return_value = {}

        ticket = Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            requester_id='1095195473',
            assignee='kan@prontomarketing.com',
            assignee_id='1095195243',
            group='Marketing Services',
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            status='open',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            stage='A',
            vertical='NASS'
        )

        response = self.client.get(
            reverse('tickets_new', kwargs={'ticket_id': ticket.id})
        )

        data = {
            'ticket': {
                'subject': 'Ticket 1',
                'comment': {
                    'body': 'Comment 1'
                },
                'requester_id': '1095195473',
                'assignee_id': '1095195243',
            }
        }
        mock.return_value.create.assert_called_once_with(data)

    @patch('tickets.views.ZendeskTicket')
    def test_ticket_new_view_should_show_result_after_send_request(self, mock):
        ticket = Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            requester_id='1095195473',
            assignee='kan@prontomarketing.com',
            assignee_id='1095195243',
            group='Marketing Services',
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            status='open',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            stage='A',
            vertical='NASS'
        )

        ticket_url = 'https://pronto1445242156.zendesk.com/api/v2/' \
            'tickets/16.json'
        result = {
            'ticket': {
                'subject': 'Hello',
                'submitter_id': 1095195473,
                'priority': None,
                'raw_subject': 'Hello',
                'id': 16,
                'url': ticket_url,
                'group_id': 23338833,
                'tags': [],
                'assignee_id': 1095195243,
                'via': {
                    'channel': 'api',
                    'source': {
                        'from': {}, 'to': {}, 'rel': None
                    }
                },
                'ticket_form_id': None,
                'updated_at': '2016-12-11T13:27:12Z',
                'created_at': '2016-12-11T13:27:12Z',
                'description': 'yeah..',
                'status': 'open',
                'requester_id': 1095195473,
                'forum_topic_id': None
            }
        }
        mock.return_value.create.return_value = result

        response = self.client.get(
            reverse('tickets_new', kwargs={'ticket_id': ticket.id})
        )

        self.assertDictEqual(
            result,
            json.loads(response.content.decode('utf-8'))
        )
