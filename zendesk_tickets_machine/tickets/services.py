import datetime
from django.utils.timezone import utc

from .models import Ticket

class TicketServices():

    def edit_ticket_once(self, id_list, edit_tags, edit_subject, edit_due_at, edit_assignee):
        if edit_tags:
                Ticket.objects.filter(pk__in=id_list).update(tags=edit_tags)
        if edit_subject:
            Ticket.objects.filter(pk__in=id_list).update(subject=edit_subject)
        if edit_due_at:
            Ticket.objects.filter(pk__in=id_list).update(
                due_at=datetime.datetime.strptime(edit_due_at, "%m/%d/%Y").replace(
                tzinfo=utc))
        if edit_assignee:
            Ticket.objects.filter(pk__in=id_list).update(assignee=edit_assignee)