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
            'group',
            'ticket_type',
            'priority',
            'tags',
            'private_comment',
            'zendesk_ticket_id',
            'board',
        ]
        widgets = {'board': forms.HiddenInput()}
