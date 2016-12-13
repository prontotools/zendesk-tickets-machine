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
            '<th>Zendesk Ticket ID</th>'
        self.assertContains(response, expected, count=2, status_code=200)

        expected = '<th></th>' \
            '<th>Subject</th>' \
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
            '<th>Zendesk Ticket ID</th>'
        self.assertContains(response, expected, count=1, status_code=200)

    def test_ticket_view_should_have_create_tickets_link(self):
        response = self.client.get(reverse('tickets'))

        expected = '<a href="%s">' \
            'Create Tickets</a>' % reverse('zendesk_tickets_create')
        self.assertContains(response, expected, count=1, status_code=200)

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

        expected = '<input type="submit">'
        self.assertContains(response, expected, status_code=200)

    def test_ticket_view_should_show_ticket_list(self):
        first_ticket = Ticket.objects.create(
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
            zendesk_ticket_id='24328'
        )
        second_ticket = Ticket.objects.create(
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
            zendesk_ticket_id='24328'
        )

        response = self.client.get(reverse('tickets'))

        expected = '<tr><td><a href="/tickets/%s/">Edit</a> | ' \
            '<a href="/tickets/%s/delete/">Delete</a></td>' \
            '<td>Ticket 1</td><td>Comment 1</td>' \
            '<td>client@hisotech.com</td><td>1095195473</td>' \
            '<td>kan@prontomarketing.com</td><td>1095195243</td>' \
            '<td>Marketing Services</td><td>question</td><td>urgent</td>' \
            '<td>welcome</td><td>open</td><td>Private comment</td>' \
            '<td>24328</td></tr>' % (
                first_ticket.id,
                first_ticket.id
            )
        self.assertContains(response, expected, status_code=200)

        expected = '<tr><td><a href="/tickets/%s/">Edit</a> | ' \
            '<a href="/tickets/%s/delete/">Delete</a></td>' \
            '<td>Ticket 2</td><td>Comment 2</td>' \
            '<td>client+another@hisotech.com</td><td>1095195474</td>' \
            '<td>kan+another@prontomarketing.com</td><td>1095195244</td>' \
            '<td>Marketing Services</td><td>question</td><td>high</td>' \
            '<td>welcome internal</td><td>open</td>' \
            '<td>Private comment</td><td>24328</td></tr>' % (
                second_ticket.id,
                second_ticket.id
            )
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
            'zendesk_ticket_id': '24328'
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

        expected = '<form method="post">'
        self.assertContains(response, expected, status_code=200)

        expected = '<tr><td><a href="/tickets/%s/">Edit</a> | ' \
            '<a href="/tickets/%s/delete/">Delete</a></td>' \
            '<td>Welcome to Pronto Service</td>' \
            '<td>This is a comment.</td><td>client@hisotech.com</td>' \
            '<td>1095195473</td><td>kan@prontomarketing.com</td>' \
            '<td>1095195243</td><td>Marketing Services</td>' \
            '<td>question</td><td>urgent</td><td>welcome</td>' \
            '<td>open</td><td>Private comment</td><td>24328</td>' \
            '</tr>' % (ticket.id, ticket.id)
        self.assertContains(response, expected, status_code=200)


class TicketEditViewTest(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
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
            zendesk_ticket_id='24328'
        )

    def test_ticket_edit_view_should_be_accessible(self):
        response = self.client.get(
            reverse('ticket_edit', kwargs={'ticket_id': self.ticket.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_ticket_edit_view_should_have_back_link_to_ticket_list(self):
        response = self.client.get(
            reverse('ticket_edit', kwargs={'ticket_id': self.ticket.id})
        )

        expected = '<a href="%s">Back</a>' % reverse('tickets')
        self.assertContains(response, expected, count=1, status_code=200)

    def test_ticket_edit_view_should_have_table_header(self):
        response = self.client.get(
            reverse('ticket_edit', kwargs={'ticket_id': self.ticket.id})
        )

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
            '<th>Zendesk Ticket ID</th>'
        self.assertContains(response, expected, count=1, status_code=200)

    def test_ticket_edit_view_should_render_ticket_form(self):
        response = self.client.get(
            reverse('ticket_edit', kwargs={'ticket_id': self.ticket.id})
        )

        expected = '<form method="post">'
        self.assertContains(response, expected, status_code=200)

        expected = "<input type='hidden' name='csrfmiddlewaretoken'"
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_subject" maxlength="300" name="subject" ' \
            'type="text" value="Ticket 1" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_comment" maxlength="500" name="comment" ' \
            'type="text" value="Comment 1" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_requester" maxlength="100" ' \
            'name="requester" type="text" value="client@hisotech.com" ' \
            'required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_requester_id" maxlength="50" ' \
            'name="requester_id" type="text" value="1095195473" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_assignee" maxlength="100" ' \
            'name="assignee" type="text" value="kan@prontomarketing.com" ' \
            'required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_assignee_id" maxlength="50" ' \
            'name="assignee_id" type="text" value="1095195243" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_group" maxlength="50" ' \
            'name="group" type="text" value="Marketing Services" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_ticket_type" maxlength="50" ' \
            'name="ticket_type" type="text" value="question" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_priority" maxlength="50" ' \
            'name="priority" type="text" value="urgent" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_tags" maxlength="300" name="tags" ' \
            'type="text" value="welcome" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_status" maxlength="300" name="status" ' \
            'type="text" value="open" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_private_comment" maxlength="500" ' \
            'name="private_comment" type="text" value="Private comment" ' \
            'required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_zendesk_ticket_id" maxlength="50" ' \
            'name="zendesk_ticket_id" type="text" value="24328" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="submit">'
        self.assertContains(response, expected, status_code=200)

    def test_ticket_edit_view_should_save_data_and_redirect_to_ticket_view(
        self
    ):
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
            'zendesk_ticket_id': '24328'
        }

        response = self.client.post(
            reverse('ticket_edit', kwargs={'ticket_id': self.ticket.id}),
            data=data
        )

        ticket = Ticket.objects.get(id=self.ticket.id)

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

        self.assertRedirects(
            response,
            reverse('tickets'),
            status_code=302,
            target_status_code=200
        )


class TicketDeleteViewTest(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
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
            zendesk_ticket_id='24328'
        )

    def test_ticket_delete_view_should_delete_and_redirect_to_ticket_view(
        self
    ):
        response = self.client.get(
            reverse('ticket_delete', kwargs={'ticket_id': self.ticket.id})
        )

        self.assertEqual(Ticket.objects.count(), 0)

        self.assertRedirects(
            response,
            reverse('tickets'),
            status_code=302,
            target_status_code=200
        )
