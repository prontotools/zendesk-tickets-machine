from django.core.urlresolvers import reverse
from django.test import TestCase


class TicketViewTest(TestCase):
    def test_ticket_view_should_be_accessiable(self):
        response = self.client.get(reverse('tickets'))
        self.assertEqual(response.status_code, 200)
