from django.contrib.auth.models import User
from django.test import TestCase

from ..models import BoardGroup


class BoardGroupAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.url = '/admin/board_groups/boardgroup/'

    def test_access_board_group_admin_should_have_columns(self):
        BoardGroup.objects.create(name='CP Production')
        response = self.client.get(self.url)

        expected = '<div class="text"><a href="?o=1">Name</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)
