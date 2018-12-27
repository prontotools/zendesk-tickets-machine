from django.test import TestCase

from ..models import AgentGroup


class AgentGroupTest(TestCase):
    def test_save_agent_group(self):
        agent_group = AgentGroup()
        agent_group.name = 'Development'
        agent_group.zendesk_group_id = '25050306'
        agent_group.save()

        agent_group = AgentGroup.objects.last()

        self.assertEqual(agent_group.name, 'Development')
        self.assertEqual(agent_group.zendesk_group_id, '25050306')

    def test_agent_group_should_represent_name_by_default(self):
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='25050306'
        )
        self.assertEqual(agent_group.__str__(), 'Development')
