from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Board, BoardGroup


class BoardAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.url = '/admin/boards/board/'

    def test_access_board_admin_should_have_columns(self):
        Board.objects.create(
            name='Pre-Production',
            slug='pre-production'
        )
        response = self.client.get(self.url)

        expected = '<div class="text"><a href="?o=1">Name</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=2">Slug</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=3">Board group</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)


class BoardGroupAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.url = '/admin/boards/boardgroup/'

    def test_access_board_group_admin_should_have_columns(self):
        BoardGroup.objects.create(name='CP Production')
        response = self.client.get(self.url)

        expected = '<div class="text"><a href="?o=1">Name</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)
