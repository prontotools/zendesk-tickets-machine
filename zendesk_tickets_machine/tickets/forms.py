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
            'ticket_type',
            'priority',
            'tags',
        ]
