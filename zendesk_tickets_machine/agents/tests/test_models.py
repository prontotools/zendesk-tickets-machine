from django.test import TestCase

from ..models import Agent


class AgentTest(TestCase):
    def test_save_agent(self):
        agent = Agent()
        agent.name = 'Kan Ouivirach'
        agent.zendesk_user_id = '403620641'
        agent.save()

        agent = Agent.objects.last()

        self.assertEqual(agent.name, 'Kan Ouivirach')
        self.assertEqual(agent.zendesk_user_id, '403620641')
