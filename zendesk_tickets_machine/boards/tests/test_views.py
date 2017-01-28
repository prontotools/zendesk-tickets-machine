import datetime

from unittest.mock import call, patch

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.timezone import utc

from ..models import Board, BoardGroup
from agents.models import Agent
from agent_groups.models import AgentGroup
from requesters.models import Requester
from tickets.models import Ticket


class BoardViewTest(TestCase):

    def login(self):
        User.objects.create_superuser('natty', 'natty@test', 'pass')
        self.client.login(username='natty', password='pass')

    def test_board_view_should_have_title(self):
        self.login()
        response = self.client.get(reverse('boards'))

        expected = '<title>Pronto Zendesk Tickets Machine</title>'
        self.assertContains(response, expected, status_code=200)

    def test_board_view_should_show_boards_in_board_group(self):
        self.login()
        board_group = BoardGroup.objects.create(name='CP Production')
        first_board = Board.objects.create(
            name='Pre-Production',
            board_group=board_group
        )
        second_board = Board.objects.create(
            name='Monthly Newsletter',
            board_group=board_group
        )

        response = self.client.get(reverse('boards'))

        expected = '<h1>Boards</h1>'
        self.assertContains(response, expected, status_code=200)

        expected = '<li>CP Production</li>'
        self.assertContains(response, expected, status_code=200)

        expected = '<li><a href="%s">%s</a></li>' % (
            reverse(
                'board_single', kwargs={'slug': first_board.slug}
            ),
            first_board.name
        )
        self.assertContains(response, expected, status_code=200)

        expected = '<li><a href="%s">%s</a></li>' % (
            reverse(
                'board_single', kwargs={'slug': second_board.slug}
            ),
            second_board.name
        )
        self.assertContains(response, expected, status_code=200)

    def test_board_view_should_show_ungrouped_boards(self):
        self.login()
        board = Board.objects.create(name='Pre-Production')

        response = self.client.get(reverse('boards'))

        expected = '<h1>Boards</h1>'
        self.assertContains(response, expected, status_code=200)

        expected = '<li>Undefined Group</li>'
        self.assertContains(response, expected, status_code=200)

        expected = '<li><a href="%s">%s</a></li>' % (
            reverse(
                'board_single', kwargs={'slug': board.slug}
            ),
            board.name
        )
        self.assertContains(response, expected, status_code=200)

    def test_board_view_should_have_logout(self):
        self.login()
        Board.objects.create(name='Pre-Production')

        response = self.client.get(reverse('boards'))

        expected = '<a href="/logout/">logout</a>'
        self.assertContains(response, expected, status_code=200)

    def test_board_view_should_required_login(self):
        with self.settings(LOGIN_URL=reverse('login')):
            response = self.client.get('/')
            self.assertRedirects(response, '/login/?next=/')


class BoardSingleViewTest(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(name='Natty', zendesk_user_id='456')
        self.agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        self.board = Board.objects.create(name='Pre-Production')
        self.first_ticket = Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            assignee=self.agent,
            group=self.agent_group,
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            board=self.board
        )
        board = Board.objects.create(name='Production')
        self.second_ticket = Ticket.objects.create(
            subject='Ticket 2',
            comment='Comment 2',
            requester='client+another@hisotech.com',

            assignee=self.agent,
            group=self.agent_group,
            ticket_type='question',
            priority='high',
            tags='welcome internal',
            private_comment='Private comment',
            board=board
        )

    def login(self):
        User.objects.create_superuser('natty', 'natty@test', 'pass')
        self.client.login(username='natty', password='pass')

    def test_board_single_view_should_have_title_with_board_name(self):
        self.login()
        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )
        expected = '<title>%s | Pronto Zendesk Tickets Machine' \
            '</title>' % self.board.name
        self.assertContains(response, expected, status_code=200)

    def test_board_single_view_should_render_ticket_form(self):
        self.login()
        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )

        expected = '<form method="post">'
        self.assertContains(response, expected, status_code=200)

        expected = "<input type='hidden' name='csrfmiddlewaretoken'"
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="text" name="subject" placeholder="Subject" ' \
            'class="form-control" maxlength="300" required id="id_subject" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="text" name="requester" ' \
            'placeholder="Requester" class="form-control" maxlength="100" ' \
            'required id="id_requester" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<textarea name="comment" cols="40" rows="6" ' \
            'placeholder="Comment" class="form-control" required ' \
            'id="id_comment">\n</textarea>'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="text" name="tags" placeholder="Tags" ' \
            'class="form-control" maxlength="300" id="id_tags" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<select name="assignee" class="form-control" ' \
            'id="id_assignee">'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="1">Natty</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<select name="group" class="form-control" ' \
            'required id="id_group">'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="1">Development</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<select name="ticket_type" class="form-control" ' \
            'onChange="check_ticket_type()" id="id_ticket_type">'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="question">Question</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="incident">Incident</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="problem">Problem</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="task">Task</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<div class="form-group" id="due_at" style="display:none">'
        self.assertContains(response, expected, status_code=200)
        expected = '<input type="text" name="due_at" class="form-control" ' \
            'size="10" id="datepicker" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<select name="priority" class="form-control" ' \
            'required id="id_priority">'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="high">High</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="urgent">Urgent</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="normal">Normal</option>'
        self.assertContains(response, expected, status_code=200)
        expected = '<option value="low">Low</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<textarea name="private_comment" cols="40" rows="13" ' \
            'placeholder="Private Comment" class="form-control" ' \
            'id="id_private_comment">'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="hidden" name="board" value="%s" ' \
            'id="id_board" />' % self.board.id
        self.assertContains(response, expected, status_code=200)

        expected = '<button type="submit" class="btn btn-default">' \
            'Add New Ticket</button>'
        self.assertContains(response, expected, status_code=200)

    def test_board_single_view_should_have_table_header(self):
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

    def test_board_single_view_should_have_create_tickets_link(self):
        self.login()
        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )

        expected = '<a href="%s">Create Tickets</a>' % reverse(
            'board_tickets_create',
            kwargs={'slug': self.board.slug}
        )
        self.assertContains(response, expected, count=1, status_code=200)

    def test_board_single_view_should_have_reset_form_link(self):
        self.login()
        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )

        expected = '<a href="%s">' \
            'Reset Tickets</a>' % reverse(
                'board_reset',
                kwargs={'slug': self.board.slug}
            )
        self.assertContains(response, expected, count=1, status_code=200)

    def test_board_single_view_should_have_board_name(self):
        self.login()
        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )

        expected = '<h1>%s</h1>' % self.board.name
        self.assertContains(response, expected, status_code=200)

    def test_board_single_view_should_show_ticket_list(self):
        self.login()
        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )

        expected = '<tr><td><a href="%s">Edit</a> | ' \
            '<a href="%s">Delete</a></td>' \
            '<td>Ticket 1</td><td>Comment 1</td>' \
            '<td>client@hisotech.com</td>' \
            '<td>Natty</td><td>Development</td>' \
            '<td>question</td><td></td>' \
            '<td>urgent</td><td>welcome</td>' \
            '<td>Private comment</td>' \
            '<td><a href="%s" target="_blank">24328</a></td></tr>' % (
                reverse(
                    'ticket_edit',
                    kwargs={'ticket_id': self.first_ticket.id}
                ),
                reverse(
                    'ticket_delete',
                    kwargs={'ticket_id': self.first_ticket.id}
                ),
                settings.ZENDESK_URL + '/agent/tickets/24328'
            )
        self.assertContains(response, expected, status_code=200)

        expected = '<tr><td><a href="/%s/">Edit</a> | ' \
            '<a href="/%s/delete/">Delete</a></td>' \
            '<td>Ticket 2</td><td>Comment 2</td>' \
            '<td>client+another@hisotech.com</td><td>1095195474</td>' \
            '<td>Natty</td><td>Development</td>' \
            '<td>question</td><td>None</td>' \
            '<td>urgent</td><td>welcome internal</td>' \
            '<td>Private comment</td>' \
            '<td></td></tr>' % (
                self.second_ticket.id,
                self.second_ticket.id
            )
        self.assertNotContains(response, expected, status_code=200)

    def test_board_single_view_should_have_date_format(self):
        self.login()
        due_at = datetime.datetime(2017, 1, 1, 12, 30, 59, 0).replace(
            tzinfo=utc
        )
        Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            assignee=self.agent,
            group=self.agent_group,
            ticket_type='question',
            due_at=due_at,
            priority='urgent',
            tags='welcome',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            board=self.board
        )
        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )
        expected = '<td>Jan 01, 2017</td>'
        self.assertContains(response, expected, status_code=200)

    def test_board_single_view_should_show_ticket_type_as_dashes_if_no_value(
        self
    ):
        self.login()
        self.first_ticket.ticket_type = None
        self.first_ticket.save()

        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )

        expected = '<tr><td><a href="%s">Edit</a> | ' \
            '<a href="%s">Delete</a></td>' \
            '<td>Ticket 1</td><td>Comment 1</td>' \
            '<td>client@hisotech.com</td>' \
            '<td>Natty</td><td>Development</td>' \
            '<td>---</td><td></td>' \
            '<td>urgent</td><td>welcome</td>' \
            '<td>Private comment</td>' \
            '<td><a href="%s" target="_blank">24328</a></td></tr>' % (
                reverse(
                    'ticket_edit',
                    kwargs={'ticket_id': self.first_ticket.id}
                ),
                reverse(
                    'ticket_delete',
                    kwargs={'ticket_id': self.first_ticket.id}
                ),
                settings.ZENDESK_URL + '/agent/tickets/24328'
            )
        self.assertContains(response, expected, status_code=200)

        expected = '<tr><td><a href="/%s/">Edit</a> | ' \
            '<a href="/%s/delete/">Delete</a></td>' \
            '<td>Ticket 2</td><td>Comment 2</td>' \
            '<td>client+another@hisotech.com</td><td>1095195474</td>' \
            '<td>Natty</td><td>Development</td>' \
            '<td>question</td><td>None</td>' \
            '<td>urgent</td><td>welcome internal</td>' \
            '<td>Private comment</td>' \
            '<td></td></tr>' % (
                self.second_ticket.id,
                self.second_ticket.id
            )
        self.assertNotContains(response, expected, status_code=200)

    def test_board_single_view_should_show_assignee_as_dashes_if_no_value(
        self
    ):
        self.login()
        self.first_ticket.assignee = None
        self.first_ticket.save()

        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )

        expected = '<tr><td><a href="%s">Edit</a> | ' \
            '<a href="%s">Delete</a></td>' \
            '<td>Ticket 1</td><td>Comment 1</td>' \
            '<td>client@hisotech.com</td>' \
            '<td>---</td><td>Development</td>' \
            '<td>question</td><td></td>' \
            '<td>urgent</td><td>welcome</td>' \
            '<td>Private comment</td>' \
            '<td><a href="%s" target="_blank">24328</a></td></tr>' % (
                reverse(
                    'ticket_edit',
                    kwargs={'ticket_id': self.first_ticket.id}
                ),
                reverse(
                    'ticket_delete',
                    kwargs={'ticket_id': self.first_ticket.id}
                ),
                settings.ZENDESK_URL + '/agent/tickets/24328'
            )
        self.assertContains(response, expected, status_code=200)

        expected = '<tr><td><a href="/%s/">Edit</a> | ' \
            '<a href="/%s/delete/">Delete</a></td>' \
            '<td>Ticket 2</td><td>Comment 2</td>' \
            '<td>client+another@hisotech.com</td><td>1095195474</td>' \
            '<td>Natty</td><td>Development</td>' \
            '<td>question</td><td>None</td>' \
            '<td>urgent</td><td>welcome internal</td>' \
            '<td>Private comment</td>' \
            '<td></td></tr>' % (
                self.second_ticket.id,
                self.second_ticket.id
            )
        self.assertNotContains(response, expected, status_code=200)

    def test_board_single_view_should_save_data_when_submit_ticket_form(self):
        self.login()
        data = {
            'subject': 'Welcome to Pronto Service',
            'comment': 'This is a comment.',
            'requester': 'client@hisotech.com',
            'assignee': self.agent.id,
            'group': self.agent_group.id,
            'ticket_type': 'question',
            'priority': 'urgent',
            'tags': 'welcome',
            'private_comment': 'Private comment',
            'zendesk_ticket_id': '24328',
            'board': self.board.id
        }

        response = self.client.post(
            reverse('board_single', kwargs={'slug': self.board.slug}),
            data=data
        )

        ticket = Ticket.objects.last()

        self.assertEqual(ticket.subject, 'Welcome to Pronto Service')
        self.assertEqual(ticket.comment, 'This is a comment.')
        self.assertEqual(ticket.requester, 'client@hisotech.com')
        self.assertEqual(ticket.assignee.name, 'Natty')
        self.assertEqual(ticket.group.name, 'Development')
        self.assertEqual(ticket.ticket_type, 'question')
        self.assertEqual(ticket.priority, 'urgent')
        self.assertEqual(ticket.tags, 'welcome')
        self.assertEqual(ticket.private_comment, 'Private comment')
        self.assertEqual(ticket.zendesk_ticket_id, '24328')

        expected = '<h1>%s</h1>' % self.board.name
        self.assertContains(response, expected, status_code=200)

        expected = '<tr><td><a href="%s">Edit</a> | ' \
            '<a href="%s">Delete</a></td>' \
            '<td>Ticket 1</td><td>Comment 1</td>' \
            '<td>client@hisotech.com</td>' \
            '<td>Natty</td><td>Development</td>' \
            '<td>question</td><td></td>' \
            '<td>urgent</td><td>welcome</td>' \
            '<td>Private comment</td>' \
            '<td><a href="%s" target="_blank">24328</a></td></tr>' % (
                reverse(
                    'ticket_edit',
                    kwargs={'ticket_id': self.first_ticket.id}
                ),
                reverse(
                    'ticket_delete',
                    kwargs={'ticket_id': self.first_ticket.id}
                ),
                settings.ZENDESK_URL + '/agent/tickets/24328'
            )
        self.assertContains(response, expected, status_code=200)

        expected = '<tr><td><a href="/%s/">Edit</a> | ' \
            '<a href="/%s/delete/">Delete</a></td>' \
            '<td>Ticket 2</td><td>Comment 2</td>' \
            '<td>client+another@hisotech.com</td>' \
            '<td>Natty</td><td>Development</td>' \
            '<td>question</td><td>None</td>' \
            '<td>urgent</td><td>welcome internal</td>' \
            '<td>Private comment</td>' \
            '<td></td></tr>' % (
                self.second_ticket.id,
                self.second_ticket.id
            )
        self.assertNotContains(response, expected, status_code=200)

    def test_board_single_should_have_logout(self):
        self.login()
        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )
        expected = '<a href="/logout/">logout</a>'
        self.assertContains(response, expected, status_code=200)

    def test_board_single_view_should_required_login(self):
        with self.settings(LOGIN_URL=reverse('login')):
            response = self.client.get(
                reverse('board_single', kwargs={'slug': self.board.slug})
            )
            self.assertRedirects(response, '/login/?next=/pre-production/')


class BoardResetViewTest(TestCase):
    def setUp(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        self.board = Board.objects.create(name='Pre-Production')
        self.first_ticket = Ticket.objects.create(
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
        board = Board.objects.create(name='Another Pre-Production')
        self.second_ticket = Ticket.objects.create(
            subject='Ticket 2',
            comment='Comment 2',
            requester='client+another@hisotech.com',
            assignee=agent,
            group=agent_group,
            ticket_type='question',
            priority='high',
            tags='welcome internal',
            private_comment='Private comment',
            zendesk_ticket_id='56578',
            board=board
        )

    def login(self):
        User.objects.create_superuser('natty', 'natty@test', 'pass')
        self.client.login(username='natty', password='pass')

    def test_reset_view_should_reset_zendesk_ticket_id_for_tickets_in_board(
        self
    ):
        self.login()
        self.client.get(
            reverse('board_reset', kwargs={'slug': self.board.slug})
        )

        first_ticket = Ticket.objects.get(id=self.first_ticket.id)
        self.assertIsNone(first_ticket.zendesk_ticket_id)

        second_ticket = Ticket.objects.get(id=self.second_ticket.id)
        self.assertEqual(second_ticket.zendesk_ticket_id, '56578')

    def test_reset_view_should_redirect_to_board(self):
        self.login()
        response = self.client.get(
            reverse('board_reset', kwargs={'slug': self.board.slug})
        )

        self.assertRedirects(
            response,
            reverse('board_single', kwargs={'slug': self.board.slug}),
            status_code=302,
            target_status_code=200
        )

    def test_reset_view_should_required_login(self):
        with self.settings(LOGIN_URL=reverse('login')):
            response = self.client.get(
                reverse('board_reset', kwargs={'slug': self.board.slug})
            )
            self.assertRedirects(
                response, '/login/?next=/pre-production/reset/')


class BoardZendeskTicketsCreateViewTest(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        self.agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        self.board = Board.objects.create(name='Production')
        self.ticket = Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            assignee=self.agent,
            group=self.agent_group,
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            private_comment='Private comment',
            board=self.board
        )

    def login(self):
        User.objects.create_superuser('natty', 'natty@test', 'pass')
        self.client.login(username='natty', password='pass')

    @override_settings(DEBUG=True)
    @patch('boards.views.ZendeskTicket')
    @patch('boards.views.ZendeskRequester')
    def test_ticket_create_view_should_send_data_to_create_zendesk_ticket(
        self,
        mock_requester,
        mock_ticket
    ):
        self.login()
        ticket = Ticket.objects.last()
        ticket.tags = 'welcome, pronto_marketing'
        ticket.save()

        mock_ticket.return_value.create.return_value = {
            'ticket': {
                'id': 1
            }
        }
        mock_requester.return_value.search.return_value = {
            'users': [{
                'id': '2'
            }]
        }

        self.client.get(
            reverse('board_tickets_create', kwargs={'slug': self.board.slug})
        )

        data = {
            'ticket': {
                'subject': 'Ticket 1',
                'comment': {
                    'body': 'Comment 1'
                },
                'requester_id': '2',
                'assignee_id': '123',
                'group_id': '123',
                'type': 'question',
                'due_at': '',
                'priority': 'urgent',
                'tags': ['welcome', 'pronto_marketing']
            }
        }

        comment = {
            'ticket': {
                'comment': {
                    'author_id': '123',
                    'body': 'Private comment',
                    'public': False
                }
            }
        }
        mock_ticket.return_value.create.assert_called_once_with(data)
        mock_ticket.return_value.create_comment.assert_called_once_with(
            comment,
            1
        )

        requester = Requester.objects.last()
        self.assertEqual(requester.zendesk_user_id, '2')

    @override_settings(DEBUG=True)
    @patch('boards.views.ZendeskTicket')
    @patch('boards.views.ZendeskRequester')
    def test_ticket_create_view_should_create_two_tickets_if_there_are_two(
        self,
        mock_requester,
        mock_ticket
    ):
        self.login()
        mock_ticket.return_value.create.return_value = {
            'ticket': {
                'id': 1
            }
        }

        mock_requester.return_value.search.return_value = {
            'users': [{
                'id': '2'
            }]
        }

        mock_ticket.return_value.create_comment.return_value = {
            'audit': {
                'events': [{
                    'public': False,
                    'body': 'Private Comment',
                    'author_id': '2'
                }]
            }
        }

        Ticket.objects.create(
            subject='Ticket 2',
            comment='Comment 2',
            requester='client@hisotech.com',
            assignee=self.agent,
            group=self.agent_group,
            ticket_type='question',
            priority='low',
            tags='welcome',
            private_comment='Private comment',
            board=self.board
        )

        self.client.get(
            reverse('board_tickets_create', kwargs={'slug': self.board.slug})
        )

        self.assertEqual(mock_ticket.return_value.create.call_count, 2)
        self.assertEqual(mock_ticket.return_value.create_comment.call_count, 2)

        ticket_calls = [
            call({
                'ticket': {
                    'subject': 'Ticket 1',
                    'comment': {
                        'body': 'Comment 1'
                    },
                    'requester_id': '2',
                    'assignee_id': '123',
                    'group_id': '123',
                    'type': 'question',
                    'due_at': '',
                    'priority': 'urgent',
                    'tags': ['welcome']
                }
            }),
            call({
                'ticket': {
                    'subject': 'Ticket 2',
                    'comment': {
                        'body': 'Comment 2'
                    },
                    'requester_id': '2',
                    'assignee_id': '123',
                    'group_id': '123',
                    'type': 'question',
                    'due_at': '',
                    'priority': 'low',
                    'tags': ['welcome']
                }
            })
        ]
        mock_ticket.return_value.create.assert_has_calls(ticket_calls)

        comment_calls = [
            call({
                'ticket': {
                    'comment': {
                        'author_id': '123',
                        'body': 'Private comment',
                        'public': False
                    }
                }
            }, 1),
            call({
                'ticket': {
                    'comment': {
                        'author_id': '123',
                        'body': 'Private comment',
                        'public': False
                    }
                }
            }, 1)
        ]
        mock_ticket.return_value.create_comment.assert_has_calls(comment_calls)

        requester = Requester.objects.last()
        self.assertEqual(requester.zendesk_user_id, '2')

    @override_settings(DEBUG=True)
    @patch('boards.views.ZendeskTicket')
    @patch('boards.views.ZendeskRequester')
    def test_ticket_create_view_should_create_only_tickets_in_their_board(
        self,
        mock_requester,
        mock_ticket
    ):
        self.login()
        mock_ticket.return_value.create.return_value = {
            'ticket': {
                'id': 1
            }
        }

        mock_requester.return_value.search.return_value = {
            'users': [{
                'id': '2'
            }]
        }

        mock_ticket.return_value.create_comment.return_value = {
            'audit': {
                'events': [{
                    'public': False,
                    'body': 'Private Comment',
                    'author_id': '2'
                }]
            }
        }

        board = Board.objects.create(name='Monthly Newsletter')
        Ticket.objects.create(
            subject='Ticket 2',
            comment='Comment 2',
            requester='client@hisotech.com',
            assignee=self.agent,
            group=self.agent_group,
            ticket_type='question',
            priority='low',
            tags='welcome',
            private_comment='Private comment',
            board=board
        )

        self.client.get(
            reverse('board_tickets_create', kwargs={'slug': self.board.slug})
        )

        self.assertEqual(mock_ticket.return_value.create.call_count, 1)
        self.assertEqual(mock_ticket.return_value.create_comment.call_count, 1)

        ticket_calls = [
            call({
                'ticket': {
                    'subject': 'Ticket 1',
                    'comment': {
                        'body': 'Comment 1'
                    },
                    'requester_id': '2',
                    'assignee_id': '123',
                    'group_id': '123',
                    'type': 'question',
                    'due_at': '',
                    'priority': 'urgent',
                    'tags': ['welcome']
                }
            })
        ]
        mock_ticket.return_value.create.assert_has_calls(ticket_calls)

        comment_calls = [
            call({
                'ticket': {
                    'comment': {
                        'author_id': '123',
                        'body': 'Private comment',
                        'public': False
                    }
                }
            }, 1)
        ]
        mock_ticket.return_value.create_comment.assert_has_calls(comment_calls)

        requester = Requester.objects.last()
        self.assertEqual(requester.zendesk_user_id, '2')

    @override_settings(DEBUG=True)
    @patch('boards.views.ZendeskTicket')
    @patch('boards.views.ZendeskRequester')
    def test_ticket_create_view_should_redirect_to_board(
        self,
        mock_requester,
        mock_ticket
    ):
        self.login()
        mock_requester.return_value.search.return_value = {
            'users': [{
                'id': '1095195473'
            }]
        }
        mock_ticket.return_value.create.return_value = {
            'ticket': {
                'id': 1
            }
        }

        response = self.client.get(
            reverse('board_tickets_create', kwargs={'slug': self.board.slug})
        )

        self.assertRedirects(
            response,
            reverse('board_single', kwargs={'slug': self.board.slug}),
            status_code=302,
            target_status_code=200
        )

        requester = Requester.objects.last()
        self.assertEqual(requester.zendesk_user_id, '1095195473')

    @override_settings(DEBUG=True)
    @patch('boards.views.ZendeskTicket')
    @patch('boards.views.ZendeskRequester')
    def test_it_should_set_zendesk_ticket_id_and_requester_id_to_ticket(
        self,
        mock_requester,
        mock_ticket
    ):
        self.login()
        self.assertIsNone(self.ticket.zendesk_ticket_id)

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
                'tags': ['welcome'],
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
        mock_ticket.return_value.create.return_value = result

        mock_requester.return_value.search.return_value = {
            'users': [{
                'id': '1095195473'
            }]
        }

        self.client.get(
            reverse('board_tickets_create', kwargs={'slug': self.board.slug})
        )

        ticket = Ticket.objects.last()
        self.assertEqual(ticket.zendesk_ticket_id, '16')

        requester = Requester.objects.last()
        self.assertEqual(requester.zendesk_user_id, '1095195473')

    @patch('boards.views.ZendeskTicket')
    def test_create_view_should_not_create_if_zendesk_ticket_id_not_empty(
        self,
        mock
    ):
        self.login()
        ticket = Ticket.objects.last()
        ticket.zendesk_ticket_id = '123'
        ticket.save()

        self.client.get(
            reverse('board_tickets_create', kwargs={'slug': self.board.slug})
        )

        self.assertEqual(mock.return_value.create.call_count, 0)

    @override_settings(DEBUG=True)
    @patch('boards.views.ZendeskTicket')
    @patch('boards.views.ZendeskRequester')
    def test_create_view_should_not_create_if_requester_id_is_empty(
        self,
        mock_requester,
        mock_ticket
    ):
        self.login()
        self.assertIsNone(self.ticket.zendesk_ticket_id)

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
                'tags': ['welcome'],
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
                'requester_id': '',
                'forum_topic_id': None
            }
        }
        mock_ticket.return_value.create.return_value = result

        mock_requester.return_value.search.return_value = {
            'users': []
        }

        self.client.get(
            reverse('board_tickets_create', kwargs={'slug': self.board.slug})
        )

        ticket = Ticket.objects.last()
        self.assertIsNone(ticket.zendesk_ticket_id)

    @patch('boards.views.ZendeskRequester')
    def test_create_view_should_not_create_ticket_if_no_assignee(self, mock):
        self.login()
        self.ticket.assignee = None
        self.ticket.save()

        self.client.get(
            reverse('board_tickets_create', kwargs={'slug': self.board.slug})
        )

        self.assertEqual(mock.return_value.search.call_count, 0)
        self.assertIsNone(self.ticket.zendesk_ticket_id)

    def test_create_view_should_required_login(self):
        with self.settings(LOGIN_URL=reverse('login')):
            response = self.client.get(
                reverse('board_tickets_create',
                        kwargs={'slug': self.board.slug})
            )
            self.assertRedirects(response, '/login/?next=/production/tickets/')
