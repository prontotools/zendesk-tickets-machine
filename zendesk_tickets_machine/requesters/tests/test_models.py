from django.test import TestCase

from ..models import Requester


class RequesterTest(TestCase):
    def test_save_requester(self):
        requester = Requester()
        requester.email = 'customer@example.com'
        requester.zendesk_user_id = '1095195473'
        requester.save()

        requester = Requester.objects.last()

        self.assertEqual(requester.email, 'customer@example.com')
        self.assertEqual(requester.zendesk_user_id, '1095195473')

    def test_requester_should_represent_name_by_default(self):
        requester = Requester.objects.create(
            email='customer@example.com',
            zendesk_user_id='1095195473'
        )
        self.assertEquals(requester.__str__(), 'customer@example.com')
