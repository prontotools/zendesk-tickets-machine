import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View

from .api import Ticket as ZendeskTicket
from tickets.models import Ticket


class ZendeskTicketsCreateView(View):
    def get(self, request):
        zendesk_ticket = ZendeskTicket()

        tickets = Ticket.objects.exclude(zendesk_ticket_id__isnull=False)
        for each in tickets:
            data = {
                'ticket': {
                    'subject': each.subject,
                    'comment': {
                        'body': each.comment
                    },
                    'requester_id': each.requester_id,
                    'assignee_id': each.assignee.zendesk_user_id,
                    'group_id': each.group.zendesk_group_id,
                    'type': each.ticket_type,
                    'priority': each.priority,
                    'tags': each.tags.split()
                }
            }
            result = zendesk_ticket.create(data)
            each.zendesk_ticket_id = result['ticket']['id']
            each.save()

            if not settings.DEBUG:
                time.sleep(1)

        return HttpResponseRedirect(reverse('tickets'))
