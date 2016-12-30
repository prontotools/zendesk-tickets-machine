import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View

from .api import User as Requester
from .api import Ticket as ZendeskTicket
from tickets.models import Ticket


class ZendeskTicketsCreateView(View):
    def get(self, request):
        zendesk_ticket = ZendeskTicket()
        zendesk_user = Requester()

        tickets = Ticket.objects.exclude(zendesk_ticket_id__isnull=False)
        for each in tickets:
            requester_result = zendesk_user.search(each.requester)
            try:
                requester_id = requester_result['users'][0]['id']
                data = {
                'ticket': {
                    'subject': each.subject,
                    'comment': {
                        'body': each.comment
                    },
                    'requester_id': requester_id,
                    'assignee_id': each.assignee.zendesk_user_id,
                    'group_id': each.group.zendesk_group_id,
                    'type': each.ticket_type,
                    'priority': each.priority,
                    'tags': each.tags.split()
                    }
                }
                result = zendesk_ticket.create(data)
                each.zendesk_ticket_id = result['ticket']['id']
                each.requester_id = requester_id
                each.save()

                data = {
                'ticket': {
                    'comment': {
                        'author_id': each.assignee.zendesk_user_id,
                        'body': each.private_comment,
                        'public': False
                        }
                    }
                }
                result = zendesk_ticket.create_comment(data, each.zendesk_ticket_id)
                
            except IndexError:
                pass

            if not settings.DEBUG:
                time.sleep(1)

        return HttpResponseRedirect(reverse('tickets'))
