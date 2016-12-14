from django.contrib.auth.models import User
from django.test import TestCase

from ..models import AgentGroup


class AgentGroupAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.url = '/admin/agent_groups/agentgroup/'

    def test_access_agent_group_admin_should_have_columns(self):
        AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='25050306'
        )

        response = self.client.get(self.url)

        expected = '<div class="text"><a href="?o=1">Name</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=2">Zendesk group id</a>' \
            '</div>'
        self.assertContains(response, expected, count=1, status_code=200)
