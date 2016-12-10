from django.core.urlresolvers import reverse
from django.test import TestCase


class TicketViewTest(TestCase):
    def test_ticket_view_should_be_accessiable(self):
        response = self.client.get(reverse('tickets'))
        self.assertEqual(response.status_code, 200)

    def test_ticket_view_should_render_ticket_form(self):
        response = self.client.get(reverse('tickets'))

        expected = '<form method="post">'
        self.assertContains(response, expected, status_code=200)

        expected = "<input type='hidden' name='csrfmiddlewaretoken'"
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_subject" maxlength="300" name="subject" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_comment" maxlength="500" name="comment" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_requester" maxlength="100" name="requester" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_requester_id" maxlength="50" name="requester_id" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_assignee" maxlength="100" name="assignee" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_assignee_id" maxlength="50" name="assignee_id" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_ticket_type" maxlength="50" name="ticket_type" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_priority" maxlength="50" name="priority" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input id="id_tags" maxlength="300" name="tags" type="text" required />'
        self.assertContains(response, expected, status_code=200)

        expected = '<input type="submit">'
        self.assertContains(response, expected, status_code=200)
