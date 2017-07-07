# -*- coding: utf-8 -*-
from unittest.mock import call, patch

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.messages import constants as MSG
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

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

    def test_board_view_should_have_bulma_css(self):
        self.login()
        response = self.client.get(reverse('boards'))

        expected = '<link href="/static/css/bulma.css" ' \
            'rel="stylesheet" type="text/css"/>'
        self.assertContains(response, expected, status_code=200)

    def test_board_view_should_have_nav_bar(self):
        self.login()
        response = self.client.get(reverse('boards'))

        expected = '<nav class="nav has-shadow" id="top">' \
            '<div class="nav-left"><a class="nav-item" href="/">' \
            '<img src="/static/img/pronto-logo-header.png" ' \
            'alt="Pronto Logo"></a></div><div class="nav-right">' \
            '<strong class="nav-item">natty</strong>' \
            '<a href="%s" class="nav-item"><span>Log Out</span>' \
            '</a></div></nav>' % reverse('logout')
        self.assertContains(response, expected, status_code=200)

    def test_board_view_should_show_board_groups(self):
        BoardGroup.objects.create(name='CP Production')

        self.login()
        response = self.client.get(reverse('boards'))

        expected = '<p class="title">Boards</p>'
        self.assertContains(response, expected, status_code=200)

        expected = '<aside class="menu is-info"><ul class="menu-list">' \
            '<li><a href="#">CP Production</a></li>' \
            '<li><a href="#">Undefined Group</a></li>'
        self.assertContains(response, expected, status_code=200)

    def test_board_view_should_show_boards(self):
        first_board_group = BoardGroup.objects.create(name='CP Production')
        first_board = Board.objects.create(
            name='Pre-Production',
            board_group=first_board_group
        )
        second_board_group = BoardGroup.objects.create(name='WP Team')
        second_board = Board.objects.create(
             name='Monthly Newsletter',
             board_group=second_board_group
        )
        third_board = Board.objects.create(
             name='Undefined Taskboard'
        )

        self.login()
        response = self.client.get(reverse('boards'))

        expected = f'<li><a href="#">{first_board_group.name}</a></li>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = f'<a href="#">{first_board.name}</a>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = f'<li><a href="#">{second_board_group.name}</a></li>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = f'<a href="#">{second_board.name}</a>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = f'<li><a href="#">Undefined Group</a></li>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = f'<a href="#">{third_board.name}</a>'
        self.assertContains(response, expected, count=1, status_code=200)

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
            created_by=self.agent,
            assignee=self.agent,
            group=self.agent_group,
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            board=self.board
        )
        self.deleted_ticket = Ticket.objects.create(
            subject='Ticket (Deleted)',
            comment='Comment',
            requester='client@hisotech.com',
            created_by=self.agent,
            assignee=self.agent,
            group=self.agent_group,
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            private_comment='Private comment',
            zendesk_ticket_id='24330',
            board=self.board,
            is_active=False
        )
        board = Board.objects.create(name='Production')
        self.second_ticket = Ticket.objects.create(
            subject='Ticket 2',
            comment='Comment 2',
            requester='client+another@hisotech.com',
            created_by=self.agent,
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

    def test_board_single_view_should_redirect_to_home_if_not_exist(self):
        self.login()

        response = self.client.get(
            reverse('board_single', kwargs={'slug': 'ghost-board'}),
            follow=True
        )

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

        expected_message = 'Oops! The board you are looking for ' \
            'no longer exists..'
        self.assertEqual(messages[0].level, MSG.ERROR)
        self.assertEqual(messages[0].message, expected_message)

        self.assertRedirects(
            response,
            reverse('boards'),
            status_code=302,
            target_status_code=200
        )

        expected = '<h5 class="alert alert-danger">' \
            '%s</h5>' % expected_message
        self.assertContains(response, expected, status_code=200)

        data = {
            'subject': 'Welcome to Pronto Service',
            'comment': 'This is a comment.',
            'requester': 'client@hisotech.com',
            'created_by': self.agent.id,
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
            reverse('board_single', kwargs={'slug': 'ghost-board'}),
            data=data,
            follow=True
        )

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

        expected_message = 'Oops! The board you are looking for ' \
            'no longer exists..'
        self.assertEqual(messages[0].level, MSG.ERROR)
        self.assertEqual(messages[0].message, expected_message)

        self.assertRedirects(
            response,
            reverse('boards'),
            status_code=302,
            target_status_code=200
        )

        expected = '<h5 class="alert alert-danger">' \
            '%s</h5>' % expected_message
        self.assertContains(response, expected, status_code=200)

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

        expected = '<select name="created_by" class="form-control" ' \
            'id="id_created_by">\n  <option value="" selected>---------' \
            f'</option>\n\n  <option value="{self.agent.id}">' \
            f'{self.agent.name}</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<textarea name="comment" cols="40" rows="6" ' \
            'placeholder="Comment" class="form-control" required ' \
            'id="id_comment">\n</textarea>'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="text" name="tags" placeholder="Tags" ' \
            'class="form-control" maxlength="300" id="id_tags" />'
        self.assertContains(response, expected, status_code=200)

        expected = '<select name="assignee" class="form-control" ' \
            'id="id_assignee">\n  <option value="" selected>---------' \
            f'</option>\n\n  <option value="{self.agent.id}">' \
            f'{self.agent.name}</option>'
        self.assertContains(response, expected, status_code=200)

        expected = '<select name="group" class="form-control" ' \
            'required id="id_group">'
        self.assertContains(response, expected, status_code=200)

        expected = f'<option value="{self.agent_group.id}">' \
            f'{self.agent_group.name}</option>'
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

        expected = '<th class="check">' \
            '<input type="checkbox" name="select_all"/></th>' \
            '<th class="edit">Edit</th>' \
            '<th class="delete">Delete</th>' \
            '<th class="subject">Subject</th>' \
            '<th class="comment">Comment</th>' \
            '<th class="orderable requester">' \
            '<a href="?sort=requester">Requester</a></th>' \
            '<th class="created_by">Created By</th>' \
            '<th class="assignee">Assignee</th>' \
            '<th class="group">Group</th>' \
            '<th class="ticket_type">Ticket Type</th>' \
            '<th class="due_at">Due Date</th>' \
            '<th class="priority">Priority</th>' \
            '<th class="tags">Tags</th>' \
            '<th class="private_comment">Private Comment</th>' \
            '<th class="zendesk_ticket_id">Zendesk Ticket Id</th>'

        self.assertContains(response, expected, count=1, status_code=200)

    def test_board_single_view_should_have_create_tickets_button(self):
        self.login()
        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )

        expected = '<a href="%s" class="btn btn-success" ' \
            'style="margin-bottom: 10px;">Create Tickets</a>' % reverse(
                'board_tickets_create',
                kwargs={'slug': self.board.slug}
            )
        self.assertContains(response, expected, count=1, status_code=200)

    def test_board_single_view_should_have_reset_requesters_button(self):
        self.login()
        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )

        expected = '<a href="%s" class="btn btn-danger pull-right" ' \
            'style="margin-right: 5px;">Reset Requesters</a>' % reverse(
                'board_requesters_reset',
                kwargs={'slug': self.board.slug}
            )
        self.assertContains(response, expected, count=1, status_code=200)

    def test_board_single_view_should_have_reset_tickets_button(self):
        self.login()
        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )
        expected = '<a href="%s" class="btn btn-warning pull-right">' \
            'Reset Tickets</a>' % reverse(
                'board_reset',
                kwargs={'slug': self.board.slug}
            )
        self.assertContains(response, expected, count=1, status_code=200)

    def test_board_single_view_should_show_assignee_as_dashes_if_no_value(
        self
    ):
        self.login()
        self.first_ticket.assignee = None
        self.first_ticket.save()

        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )

        expected = '<td class="check">' \
            '<input type="checkbox" name="check" ' \
            f'value="{self.first_ticket.id}"/>' \
            '</td><td class="edit"><a href="%s">Edit</a></td>' \
            '<td class="delete"><a href="%s">Delete</a></td>' \
            '<td class="subject">Ticket 1</td>' \
            '<td class="comment">Comment 1</td>' \
            '<td class="requester">client@hisotech.com</td>' \
            '<td class="created_by">Natty</td>' \
            '<td class="assignee">-</td>' \
            '<td class="group">Development</td>' \
            '<td class="ticket_type">Question</td>' \
            '<td class="due_at">-</td>' \
            '<td class="priority">Urgent</td>' \
            '<td class="tags">welcome</td>' \
            '<td class="private_comment">Private comment</td>' \
            '<td class="zendesk_ticket_id">' \
            '<a href="%s" target="_blank">24328</a></td>' % (
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

        expected = '<td class="check">' \
            '<input type="checkbox" name="check" '\
            f'value="{self.second_ticket.id}"/>' \
            '</td><td class="edit"><a href="%s">Edit</a></td>' \
            '<td class="delete"><a href="%s">Delete</a></td>' \
            '<td class="subject">Ticket 2</td>' \
            '<td class="comment">Comment 2</td>' \
            '<td class="requester">client+another@hisotech.com</td>' \
            '<td class="created_by">1095195474</td>' \
            '<td class="assignee">Natty</td>' \
            '<td class="group">Development</td>' \
            '<td class="ticket_type">question</td>' \
            '<td class="due_at">-</td>' \
            '<td class="priority">urgent</td>' \
            '<td class="tags">welcome internal</td>' \
            '<td class="private_comment">Private comment</td>' \
            '<td class="zendesk_ticket_id">-</td>' % (
                self.second_ticket.id,
                self.second_ticket.id
            )
        self.assertNotContains(response, expected, status_code=200)

    def test_board_single_view_should_show_created_by_as_dashes_if_no_value(
        self
    ):
        self.login()
        self.first_ticket.created_by = None
        self.first_ticket.save()

        response = self.client.get(
            reverse('board_single', kwargs={'slug': self.board.slug})
        )

        expected = '<td class="check">' \
            '<input type="checkbox" name="check" '\
            f'value="{self.first_ticket.id}"/>' \
            '</td><td class="edit"><a href="%s">Edit</a></td>' \
            '<td class="delete"><a href="%s">Delete</a></td>' \
            '<td class="subject">Ticket 1</td>' \
            '<td class="comment">Comment 1</td>' \
            '<td class="requester">client@hisotech.com</td>' \
            '<td class="created_by">-</td>' \
            '<td class="assignee">Natty</td>' \
            '<td class="group">Development</td>' \
            '<td class="ticket_type">Question</td>' \
            '<td class="due_at">-</td>' \
            '<td class="priority">Urgent</td>' \
            '<td class="tags">welcome</td>' \
            '<td class="private_comment">Private comment</td>' \
            '<td class="zendesk_ticket_id">' \
            '<a href="%s" target="_blank">24328</a></td>' % (
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

        expected = '<td class="check">' \
            '<input type="checkbox" name="check" '\
            f'value="{self.second_ticket.id}"/>' \
            '</td><td class="edit"><a href="%s">Edit</a></td>' \
            '<td class="delete"><a href="%s">Delete</a></td>' \
            '<td class="subject">Ticket 2</td>' \
            '<td class="comment">Comment 2</td>' \
            '<td class="requester">client+another@hisotech.com</td>' \
            '<td class="created_by">1095195474</td>' \
            '<td class="assignee">Natty</td>' \
            '<td class="group">Development</td>' \
            '<td class="ticket_type">question</td>' \
            '<td class="due_at">-</td>' \
            '<td class="priority">urgent</td>' \
            '<td class="tags">welcome internal</td>' \
            '<td class="private_comment">Private comment</td>' \
            '<td class="zendesk_ticket_id">-</td>' % (
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
            'created_by': self.agent.id,
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
        self.assertEqual(ticket.created_by.name, 'Natty')
        self.assertEqual(ticket.assignee.name, 'Natty')
        self.assertEqual(ticket.group.name, 'Development')
        self.assertEqual(ticket.ticket_type, 'question')
        self.assertEqual(ticket.priority, 'urgent')
        self.assertEqual(ticket.tags, 'welcome')
        self.assertEqual(ticket.private_comment, 'Private comment')
        self.assertEqual(ticket.zendesk_ticket_id, '24328')

        expected = '<h1>%s</h1>' % self.board.name
        self.assertContains(response, expected, status_code=200)

        expected = '<td class="check">' \
            '<input type="checkbox" name="check" '\
            f'value="{self.first_ticket.id}"/>' \
            '</td><td class="edit"><a href="%s">Edit</a></td>' \
            '<td class="delete"><a href="%s">Delete</a></td>' \
            '<td class="subject">Ticket 1</td>' \
            '<td class="comment">Comment 1</td>' \
            '<td class="requester">client@hisotech.com</td>' \
            '<td class="created_by">Natty</td>' \
            '<td class="assignee">Natty</td>' \
            '<td class="group">Development</td>' \
            '<td class="ticket_type">Question</td>' \
            '<td class="due_at">-</td>' \
            '<td class="priority">Urgent</td>' \
            '<td class="tags">welcome</td>' \
            '<td class="private_comment">Private comment</td>' \
            '<td class="zendesk_ticket_id">' \
            '<a href="%s" target="_blank">24328</a></td>' % (
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
        expected = '<td class="check">' \
            f'<input type="checkbox" name="check" value="{ticket.id}"/></td>' \
            '<td class="edit"><a href="%s">Edit</a></td>' \
            '<td class="delete"><a href="%s">Delete</a></td>' \
            '<td class="subject">Welcome to Pronto Service</td>' \
            '<td class="comment">This is a comment.</td>' \
            '<td class="requester">client@hisotech.com</td>' \
            '<td class="created_by">Natty</td>' \
            '<td class="assignee">Natty</td>' \
            '<td class="group">Development</td>' \
            '<td class="ticket_type">Question</td>' \
            '<td class="due_at">-</td>' \
            '<td class="priority">Urgent</td>' \
            '<td class="tags">welcome</td>' \
            '<td class="private_comment">Private comment</td>' \
            '<td class="zendesk_ticket_id">' \
            '<a href="%s" target="_blank">24328</a></td>' % (
                reverse(
                    'ticket_edit',
                    kwargs={'ticket_id': ticket.id}
                ),
                reverse(
                    'ticket_delete',
                    kwargs={'ticket_id': ticket.id}
                ),
                settings.ZENDESK_URL + '/agent/tickets/24328'
            )
        self.assertContains(response, expected, status_code=200)

        expected = '<tr><td><a href="%s">Edit</a> | ' \
            '<a href="%s">Delete</a></td>' \
            '<td>Ticket (Deleted)</td><td>Comment</td>' \
            '<td>client@hisotech.com</td>' \
            '<td>Natty</td>' \
            '<td>Natty</td><td>Development</td>' \
            '<td>question</td><td></td>' \
            '<td>urgent</td><td>welcome</td>' \
            '<td>Private comment</td>' \
            '<td><a href="%s" target="_blank">24330</a></td></tr>' % (
                reverse(
                    'ticket_edit',
                    kwargs={'ticket_id': self.deleted_ticket.id}
                ),
                reverse(
                    'ticket_delete',
                    kwargs={'ticket_id': self.deleted_ticket.id}
                ),
                settings.ZENDESK_URL + '/agent/tickets/24330'
            )
        self.assertNotContains(response, expected, status_code=200)

        expected = '<tr><td><a href="/%s/">Edit</a> | ' \
            '<a href="/%s/delete/">Delete</a></td>' \
            '<td>Ticket 2</td><td>Comment 2</td>' \
            '<td>client+another@hisotech.com</td>' \
            '<td>Natty</td>' \
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


class BoardRequestersResetViewTest(TestCase):
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
            created_by=agent,
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
            created_by=agent,
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

    def test_requesters_reset_view_should_required_login(self):
        with self.settings(LOGIN_URL=reverse('login')):
            response = self.client.get(
                reverse(
                    'board_requesters_reset',
                    kwargs={'slug': self.board.slug}
                )
            )
            self.assertRedirects(
                response, '/login/?next=/pre-production/requesters/reset/'
            )

    def test_requesters_reset_view_should_reset_requesters_in_tickets_in_board(
        self
    ):
        self.login()
        self.client.get(
            reverse('board_requesters_reset', kwargs={'slug': self.board.slug})
        )

        first_ticket = Ticket.objects.get(id=self.first_ticket.id)
        self.assertEqual(first_ticket.requester, '')

        second_ticket = Ticket.objects.get(id=self.second_ticket.id)
        self.assertEqual(
            second_ticket.requester,
            'client+another@hisotech.com'
        )

    def test_requesters_reset_view_should_redirect_to_board(self):
        self.login()
        response = self.client.get(
            reverse('board_requesters_reset', kwargs={'slug': self.board.slug})
        )

        self.assertRedirects(
            response,
            reverse('board_single', kwargs={'slug': self.board.slug}),
            status_code=302,
            target_status_code=200
        )


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
            created_by=agent,
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
            created_by=agent,
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
                response, '/login/?next=/pre-production/reset/'
            )


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
            created_by=self.agent,
            assignee=self.agent,
            group=self.agent_group,
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            private_comment='Private comment',
            board=self.board
        )
        self.deleted_ticket = Ticket.objects.create(
            subject='Ticket (Deleted)',
            comment='Comment',
            requester='client@hisotech.com',
            created_by=self.agent,
            assignee=self.agent,
            group=self.agent_group,
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            private_comment='Private comment',
            board=self.board,
            is_active=False
        )

    def login(self):
        User.objects.create_superuser('natty', 'natty@test', 'pass')
        self.client.login(username='natty', password='pass')

    def test_create_view_should_required_login(self):
        with self.settings(LOGIN_URL=reverse('login')):
            response = self.client.get(
                reverse('board_tickets_create',
                        kwargs={'slug': self.board.slug})
            )
            self.assertRedirects(response, '/login/?next=/production/tickets/')

    @override_settings(DEBUG=True)
    @patch('boards.views.ZendeskTicket')
    @patch('boards.views.ZendeskRequester')
    def test_ticket_create_view_should_send_data_to_create_zendesk_ticket(
        self,
        mock_requester,
        mock_ticket
    ):
        self.login()
        ticket = Ticket.objects.get(id=self.ticket.id)
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
                    'body': 'Comment 1',
                    'author_id': '123'
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
            created_by=self.agent,
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
                    'subject': 'Ticket 2',
                    'comment': {
                        'body': 'Comment 2',
                        'author_id': '123'
                    },
                    'requester_id': '2',
                    'assignee_id': '123',
                    'group_id': '123',
                    'type': 'question',
                    'due_at': '',
                    'priority': 'low',
                    'tags': ['welcome']
                }
            }),
            call({
                'ticket': {
                    'subject': 'Ticket 1',
                    'comment': {
                        'body': 'Comment 1',
                        'author_id': '123'
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
            created_by=self.agent,
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
                        'body': 'Comment 1',
                        'author_id': '123'
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

        ticket = Ticket.objects.get(id=self.ticket.id)
        self.assertEqual(ticket.zendesk_ticket_id, '16')

        requester = Requester.objects.last()
        self.assertEqual(requester.zendesk_user_id, '1095195473')

    @patch('boards.views.ZendeskTicket')
    def test_create_view_should_not_create_if_zendesk_ticket_id_not_empty(
        self,
        mock
    ):
        self.login()
        ticket = Ticket.objects.get(id=self.ticket.id)
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

    @patch('boards.views.ZendeskRequester')
    def test_create_view_should_not_create_ticket_if_no_requester(self, mock):
        self.login()
        self.ticket.requester = ''
        self.ticket.save()

        self.client.get(
            reverse('board_tickets_create', kwargs={'slug': self.board.slug})
        )

        self.assertEqual(mock.return_value.search.call_count, 0)
        self.assertIsNone(self.ticket.zendesk_ticket_id)
