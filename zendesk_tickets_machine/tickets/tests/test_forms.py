from django.test import TestCase

from ..forms import TicketForm


class TicketFormTest(TestCase):
    def test_ticket_form_should_have_all_defined_fields(self):
        form = TicketForm()

        expected_fields = [
            'subject',
            'comment',
            'requester',
            'requester_id',
            'assignee',
            'group',
            'ticket_type',
            'priority',
            'tags',
            'private_comment',
            'zendesk_ticket_id',
            'board',
        ]
        for each in expected_fields:
            self.assertTrue(each in form.fields)

        self.assertEqual(len(form.fields), 12)
