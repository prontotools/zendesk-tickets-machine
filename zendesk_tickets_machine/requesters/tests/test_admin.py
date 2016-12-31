from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Requester


class RequesterAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.url = '/admin/requesters/requester/'

    def test_access_requester_admin_should_have_columns(self):
        Requester.objects.create(
            email='customer@example.com',
            zendesk_user_id='1095195473'
        )

        response = self.client.get(self.url)

        expected = '<div class="text"><a href="?o=1">Email</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=2">Zendesk user id</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)
