import datetime

from django.utils.timezone import utc

from .models import Ticket


class TicketServices():
    def edit_ticket_once(self, **kwargs):
        id_list = kwargs.get('id_list')
        edit_tags = kwargs.get('edit_tags')
        edit_requester = kwargs.get('edit_requester')
        edit_subject = kwargs.get('edit_subject')
        edit_due_at = kwargs.get('edit_due_at')
        edit_assignee = kwargs.get('edit_assignee')

        if edit_tags:
            Ticket.objects.filter(
                pk__in=id_list
            ).update(tags=edit_tags)
        if edit_subject:
            Ticket.objects.filter(
                pk__in=id_list
            ).update(subject=edit_subject)
        if edit_requester:
            Ticket.objects.filter(
                pk__in=id_list
            ).update(requester=edit_requester)
        if edit_due_at:
            Ticket.objects.filter(
                pk__in=id_list
            ).update(
                due_at=datetime.datetime.strptime(
                    edit_due_at, "%m/%d/%Y"
                ).replace(tzinfo=utc)
            )
        if edit_assignee:
            Ticket.objects.filter(
                pk__in=id_list
            ).update(assignee=edit_assignee)
