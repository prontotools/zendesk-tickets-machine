from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import Ticket
from agents.models import Agent
from agent_groups.models import AgentGroup


class TicketViewTest(TestCase):
    def test_ticket_view_should_be_accessible(self):
        response = self.client.get(reverse('tickets'))
        self.assertEqual(response.status_code, 200)

    def test_ticket_view_should_render_ticket_form(self):
        Agent.objects.create(name='Kan', zendesk_user_id='123')
        AgentGroup.objects.create(name='Development', zendesk_group_id='123')

        response = self.client.get(reverse('tickets'))

        expected = '<form method="post">'
        self.assertContains(response, expected, status_code=200)

        expected = "<input type='hidden' name='csrfmiddlewaretoken'"
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_subject" maxlength="300" name="subject" ' \
            'type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<textarea cols="40" id="id_comment" name="comment" ' \
            'rows="10" required>'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_requester" maxlength="100" ' \
            'name="requester" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<select id="id_assignee" name="assignee" required>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="1">Kan</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<select id="id_group" name="group" required>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="1">Development</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<select id="id_ticket_type" name="ticket_type" required>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="question">Question</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="incident">Incident</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="problem">Problem</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="task">Task</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<select id="id_priority" name="priority" required>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="high">High</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="urgent">Urgent</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="normal">Normal</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="low">Low</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_tags" maxlength="300" name="tags" ' \
            'type="text" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_private_comment" maxlength="500" ' \
            'name="private_comment" type="text" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_zendesk_ticket_id" maxlength="50" ' \
            'name="zendesk_ticket_id" type="text" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="submit">'
        self.assertContains(response, expected, status_code=200)

    def test_ticket_view_should_save_data_when_submit_form(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )

        data = {
            'subject': 'Welcome to Pronto Service',
            'comment': 'This is a comment.',
            'requester': 'client@hisotech.com',
            'requester_id': '1095195473',
            'assignee': agent.id,
            'group': agent_group.id,
            'ticket_type': 'question',
            'priority': 'urgent',
            'tags': 'welcome',
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
        self.assertEqual(ticket.assignee.name, 'Kan')
        self.assertEqual(ticket.group.name, 'Development')
        self.assertEqual(ticket.ticket_type, 'question')
        self.assertEqual(ticket.priority, 'urgent')
        self.assertEqual(ticket.tags, 'welcome')
        self.assertEqual(ticket.private_comment, 'Private comment')
        self.assertEqual(ticket.zendesk_ticket_id, '24328')

        expected = '<form method="post">'
        self.assertContains(response, expected, status_code=200)


class TicketEditViewTest(TestCase):
    def setUp(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        self.ticket = Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            requester_id='1095195473',
            assignee=agent,
            group=agent_group,
            ticket_type='question',
            priority='urgent',
            tags='welcome',
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
            '<th>Group</th>' \
            '<th>Ticket Type</th>' \
            '<th>Priority</th>' \
            '<th>Tags</th>' \
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

        expected = '<textarea cols="40" id="id_comment" name="comment" ' \
            'rows="10" required>'
        self.assertContains(response, expected, status_code=200)
        expected = 'Comment 1</textarea>'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_requester" maxlength="100" ' \
            'name="requester" type="text" value="client@hisotech.com" ' \
            'required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_requester_id" maxlength="50" ' \
            'name="requester_id" type="text" value="1095195473" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<select id="id_assignee" name="assignee" required>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="1" selected="selected">Kan</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<select id="id_group" name="group" required>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="1" selected="selected">Development</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<select id="id_ticket_type" name="ticket_type" required>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="question" selected="selected">Question' \
            '</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="incident">Incident</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="problem">Problem</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="task">Task</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<select id="id_priority" name="priority" required>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="high">High</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="urgent" selected="selected">Urgent</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="normal">Normal</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="low">Low</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_tags" maxlength="300" name="tags" ' \
            'type="text" value="welcome" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_private_comment" maxlength="500" ' \
            'name="private_comment" type="text" value="Private comment" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_zendesk_ticket_id" maxlength="50" ' \
            'name="zendesk_ticket_id" type="text" value="24328" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="submit">'
        self.assertContains(response, expected, status_code=200)

    def test_ticket_edit_view_should_save_data_and_redirect_to_ticket_view(
        self
    ):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )

        data = {
            'subject': 'Welcome to Pronto Service',
            'comment': 'This is a comment.',
            'requester': 'client@hisotech.com',
            'requester_id': '1095195473',
            'assignee': agent.id,
            'group': agent_group.id,
            'ticket_type': 'question',
            'priority': 'urgent',
            'tags': 'welcome',
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
        self.assertEqual(ticket.assignee.name, 'Kan')
        self.assertEqual(ticket.group.name, 'Development')
        self.assertEqual(ticket.ticket_type, 'question')
        self.assertEqual(ticket.priority, 'urgent')
        self.assertEqual(ticket.tags, 'welcome')
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
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        self.ticket = Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            requester_id='1095195473',
            assignee=agent,
            group=agent_group,
            ticket_type='question',
            priority='urgent',
            tags='welcome',
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


class TicketResetViewTest(TestCase):
    def setUp(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        self.ticket = Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            requester_id='1095195473',
            assignee=agent,
            group=agent_group,
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            private_comment='Private comment',
            zendesk_ticket_id='24328'
        )

    def test_ticket_reset_view_should_reset_zendesk_ticket_id_on_all_tickets(
        self
    ):
        response = self.client.get(reverse('tickets_reset'))

        ticket = Ticket.objects.last()
        self.assertIsNone(ticket.zendesk_ticket_id)

        self.assertRedirects(
            response,
            reverse('tickets'),
            status_code=302,
            target_status_code=200
        )
