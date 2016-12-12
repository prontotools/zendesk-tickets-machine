import json
from unittest.mock import call, patch

from django.core.urlresolvers import reverse
from django.test import TestCase

from tickets.models import Ticket


class ZendeskTicketsCreateViewTest(TestCase):
    @patch('zendesk.views.ZendeskTicket')
    def test_ticket_create_view_should_be_accessible(self, mock):
        mock.return_value.create.return_value = {}

        response = self.client.get(reverse('zendesk_tickets_create'))

        self.assertEqual(response.status_code, 200)

    @patch('zendesk.views.ZendeskTicket')
    def test_ticket_create_view_should_send_data_to_create_zendesk_ticket(
        self,
        mock
    ):
        mock.return_value.create.return_value = {}

        Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            requester_id='1095195473',
            assignee='kan@prontomarketing.com',
            assignee_id='1095195243',
            group='Marketing Services',
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            status='open',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            stage='A',
            vertical='NASS'
        )

        self.client.get(reverse('zendesk_tickets_create'))

        data = {
            'ticket': {
                'subject': 'Ticket 1',
                'comment': {
                    'body': 'Comment 1'
                },
                'requester_id': '1095195473',
                'assignee_id': '1095195243',
            }
        }
        mock.return_value.create.assert_called_once_with(data)

    @patch('zendesk.views.ZendeskTicket')
    def test_ticket_create_view_should_create_two_tickets_if_there_are_two(
        self,
        mock
    ):
        mock.return_value.create.return_value = {}

        Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            requester_id='1095195473',
            assignee='kan@prontomarketing.com',
            assignee_id='1095195243',
            group='Marketing Services',
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            status='open',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            stage='A',
            vertical='NASS'
        )
        Ticket.objects.create(
            subject='Ticket 2',
            comment='Comment 2',
            requester='client@hisotech.com',
            requester_id='1095195473',
            assignee='kan@prontomarketing.com',
            assignee_id='1095195243',
            group='Marketing Services',
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            status='open',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            stage='A',
            vertical='NASS'
        )

        self.client.get(reverse('zendesk_tickets_create'))

        self.assertEqual(mock.return_value.create.call_count, 2)

        calls = [
            call({
                'ticket': {
                    'subject': 'Ticket 1',
                    'comment': {
                        'body': 'Comment 1'
                    },
                    'requester_id': '1095195473',
                    'assignee_id': '1095195243',
                }
            }),
            call({
                'ticket': {
                    'subject': 'Ticket 2',
                    'comment': {
                        'body': 'Comment 2'
                    },
                    'requester_id': '1095195473',
                    'assignee_id': '1095195243',
                }
            })
        ]
        mock.return_value.create.assert_has_calls(calls)

    @patch('zendesk.views.ZendeskTicket')
    def test_ticket_create_view_should_show_results_after_send_request(
        self,
        mock
    ):
        Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            requester_id='1095195473',
            assignee='kan@prontomarketing.com',
            assignee_id='1095195243',
            group='Marketing Services',
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            status='open',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            stage='A',
            vertical='NASS'
        )

        ticket_url = 'https://pronto1445242156.zendesk.com/api/v2/' \
            'tickets/16.json'
        result = {
            'ticket': {
                'subject': 'Hello',
                'submitter_id': 1095195473,
                'priority': None,
                'raw_subject': 'Hello',
                'id': 16,
                'url': ticket_url,
                'group_id': 23338833,
                'tags': [],
                'assignee_id': 1095195243,
                'via': {
                    'channel': 'api',
                    'source': {
                        'from': {}, 'to': {}, 'rel': None
                    }
                },
                'ticket_form_id': None,
                'updated_at': '2016-12-11T13:27:12Z',
                'created_at': '2016-12-11T13:27:12Z',
                'description': 'yeah..',
                'status': 'open',
                'requester_id': 1095195473,
                'forum_topic_id': None
            }
        }
        results = {
            'results': [result]
        }
        mock.return_value.create.return_value = result

        response = self.client.get(reverse('zendesk_tickets_create'))

        self.assertDictEqual(
            results,
            json.loads(response.content.decode('utf-8'))
        )
