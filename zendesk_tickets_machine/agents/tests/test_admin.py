from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Agent


class AgentAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.url = '/admin/agents/agent/'

    def test_access_agent_admin_should_have_columns(self):
        Agent.objects.create(
            name='Kan Ouivirach',
            zendesk_user_id='403620641'
        )

        response = self.client.get(self.url)

        expected = '<div class="text"><a href="?o=1">Name</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=2">Zendesk user id</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)
