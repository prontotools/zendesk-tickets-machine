from django import forms

from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'subject',
            'comment',
            'requester',
            'requester_id',
            'assignee',
            'assignee_id',
            'group',
            'ticket_type',
            'priority',
            'tags',
            'status',
            'private_comment',
            'zendesk_ticket_id',
            'stage',
            'vertical',
        ]
