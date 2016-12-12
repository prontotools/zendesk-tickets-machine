import time

from django.conf import settings
from django.http import JsonResponse
from django.test.utils import override_settings
from django.views.generic import View

from .api import Ticket as ZendeskTicket
from tickets.models import Ticket


class ZendeskTicketsCreateView(View):
    def get(self, request):
        zendesk_ticket = ZendeskTicket()

        results = {'results': []}
        tickets = Ticket.objects.all()
        for each in tickets:
            data = {
                'ticket': {
                    'subject': each.subject,
                    'comment': {
                        'body': each.comment
                    },
                    'requester_id': each.requester_id,
                    'assignee_id': each.assignee_id,
                }
            }
            result = zendesk_ticket.create(data)
            results['results'].append(result)

            if not settings.DEBUG:
                time.sleep(1)

        return JsonResponse(results)
