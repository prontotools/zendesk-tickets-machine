from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import Ticket
from agents.models import Agent
from agent_groups.models import AgentGroup
from boards.models import Board


class TicketEditViewTest(TestCase):
    def setUp(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        self.board = Board.objects.create(name='Pre-Production')
        self.ticket = Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            assignee=agent,
            group=agent_group,
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            board=self.board
        )

    def login(self):
        User.objects.create_superuser('natty', 'natty@test', 'pass')
        self.client.login(username='natty', password='pass')

    def test_ticket_edit_view_should_be_accessible(self):
        self.login()
        response = self.client.get(
            reverse('ticket_edit', kwargs={'ticket_id': self.ticket.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_ticket_edit_view_should_have_back_link_to_ticket_list(self):
        self.login()
        response = self.client.get(
            reverse('ticket_edit', kwargs={'ticket_id': self.ticket.id})
        )

        expected = '<a href="%s">Back</a>' % reverse(
            'board_single',
            kwargs={'slug': self.ticket.board.slug}
        )
        self.assertContains(response, expected, count=1, status_code=200)

    def test_ticket_edit_view_should_have_table_header(self):
        self.login()
        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )

        expected = '<table class="table table-bordered table-condensed ' \
            'table-hover">'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<th width="7%"></th>' \
            '<th>Subject</th>' \
            '<th>Comment</th>' \
            '<th>Requester</th>' \
            '<th>Assignee</th>' \
            '<th>Group</th>' \
            '<th>Ticket Type</th>' \
            '<th>Due Date</th>' \
            '<th>Priority</th>' \
            '<th>Tags</th>' \
            '<th>Private Comment</th>' \
            '<th>Zendesk Ticket ID</th>'
        self.assertContains(response, expected, count=1, status_code=200)

    def test_ticket_edit_view_should_render_ticket_form(self):
        self.login()
        response = self.client.get(
            reverse('ticket_edit', kwargs={'ticket_id': self.ticket.id})
        )

        expected = '<form method="post">'
        self.assertContains(response, expected, status_code=200)

        expected = "<input type='hidden' name='csrfmiddlewaretoken'"
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="text" name="subject" value="Ticket 1" ' \
            'placeholder="Subject" class="form-control" maxlength="300" ' \
            'required id="id_subject" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<textarea name="comment" cols="40" rows="6" ' \
            'placeholder="Comment" class="form-control" required ' \
            'id="id_comment">\nComment 1</textarea>'
        self.assertContains(response, expected, status_code=200)
        expected = 'Comment 1</textarea>'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="text" name="requester" ' \
            'value="client@hisotech.com" placeholder="Requester" ' \
            'class="form-control" maxlength="100" required ' \
            'id="id_requester" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<select name="assignee" class="form-control" ' \
            'id="id_assignee">'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="1" selected>Kan</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<select name="group" class="form-control" ' \
            'required id="id_group">'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="1" selected>Development</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<select name="ticket_type" class="form-control" ' \
            'onChange="check_ticket_type()" id="id_ticket_type">'
        self.assertContains(response, expected, status_code=200)
        expected = '<input type="text" name="due_at" class="form-control" ' \
            'size="10" id="datepicker" />'
        self.assertContains(response, expected, status_code=200)
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="question" selected>Question</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="incident">Incident</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="problem">Problem</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="task">Task</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<select name="priority" class="form-control" ' \
            'required id="id_priority">'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="high">High</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="urgent" selected>Urgent</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="normal">Normal</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="low">Low</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="text" name="tags" value="welcome" ' \
            'placeholder="Tags" class="form-control" maxlength="300" ' \
            'id="id_tags" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<textarea name="private_comment" cols="40" ' \
            'rows="13" placeholder="Private Comment" class="form-control" ' \
            'id="id_private_comment">\nPrivate comment</textarea>'
        self.assertContains(response, expected, status_code=200)
        expected = 'Private comment</textarea>'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="text" name="zendesk_ticket_id" ' \
            'value="24328" maxlength="50" id="id_zendesk_ticket_id" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="hidden" name="board" value="%s" ' \
            'id="id_board" />' % self.board.id
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="submit" class="btn btn-default" />'
        self.assertContains(response, expected, status_code=200)

    def test_ticket_edit_view_should_save_data_and_redirect_to_its_board(self):
        self.login()
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )

        data = {
            'subject': 'Welcome to Pronto Service',
            'comment': 'This is a comment.',
            'requester': 'client@hisotech.com',
            'assignee': agent.id,
            'group': agent_group.id,
            'ticket_type': 'question',
            'priority': 'urgent',
            'tags': 'welcome',
            'private_comment': 'Private comment',
            'zendesk_ticket_id': '24328',
            'board': self.board.id
        }

        response = self.client.post(
            reverse('ticket_edit', kwargs={'ticket_id': self.ticket.id}),
            data=data
        )

        ticket = Ticket.objects.get(id=self.ticket.id)

        self.assertEqual(ticket.subject, 'Welcome to Pronto Service')
        self.assertEqual(ticket.comment, 'This is a comment.')
        self.assertEqual(ticket.requester, 'client@hisotech.com')
        self.assertEqual(ticket.assignee.name, 'Kan')
        self.assertEqual(ticket.group.name, 'Development')
        self.assertEqual(ticket.ticket_type, 'question')
        self.assertEqual(ticket.priority, 'urgent')
        self.assertEqual(ticket.tags, 'welcome')
        self.assertEqual(ticket.private_comment, 'Private comment')
        self.assertEqual(ticket.zendesk_ticket_id, '24328')
        self.assertEqual(ticket.board.id, self.board.id)

        self.assertRedirects(
            response,
            reverse('board_single', kwargs={'slug': ticket.board.slug}),
            status_code=302,
            target_status_code=200
        )

    def test_ticket_edit_view_should_required_login(self):
        with self.settings(LOGIN_URL=reverse('login')):
            response = self.client.get(
                reverse('ticket_edit',
                        kwargs={'ticket_id': self.ticket.id})
            )
            self.assertRedirects(response, '/login/?next=/tickets/1/')


class TicketDeleteViewTest(TestCase):
    def setUp(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        self.board = Board.objects.create(name='Pre-Production')
        self.ticket = Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            assignee=agent,
            group=agent_group,
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            board=self.board
        )

    def login(self):
        User.objects.create_superuser('natty', 'natty@test', 'pass')
        self.client.login(username='natty', password='pass')

    def test_ticket_delete_view_should_delete_then_redirect_to_its_board(self):
        self.login()
        response = self.client.get(
            reverse('ticket_delete', kwargs={'ticket_id': self.ticket.id})
        )

        self.assertEqual(Ticket.objects.count(), 0)

        self.assertRedirects(
            response,
            reverse('board_single', kwargs={'slug': self.ticket.board.slug}),
            status_code=302,
            target_status_code=200
        )

    def test_ticket_delete_view_should_required_login(self):
        with self.settings(LOGIN_URL=reverse('login')):
            response = self.client.get(
                reverse('ticket_delete',
                        kwargs={'ticket_id': self.ticket.id})
            )
            self.assertRedirects(response, '/login/?next=/tickets/1/delete/')
