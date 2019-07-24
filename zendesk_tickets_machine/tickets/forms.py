from django import forms
from django.contrib.admin import widgets

from .models import Ticket
from agents.models import Agent


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Ticket
        fields = [
            'subject',
            'comment',
            'requester',
            'created_by',
            'assignee',
            'group',
            'ticket_type',
            'due_at',
            'priority',
            'tags',
            'private_comment',
            'zendesk_ticket_id',
            'cycle',
            'board',
        ]
        widgets = {
            'subject': forms.TextInput(
                attrs={
                    'placeholder': 'Subject',
                    'class': 'form-control'
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'placeholder': 'Comment',
                    'class': 'form-control',
                    'rows': 6
                }
            ),
            'requester': forms.TextInput(
                attrs={
                    'placeholder': 'Requester',
                    'class': 'form-control'
                }
            ),
            'created_by': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'assignee': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'group': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'ticket_type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'onChange': 'check_ticket_type()'
                }
            ),
            'due_at': widgets.AdminDateWidget(
                attrs={
                    'class': 'form-control',
                    'id': 'datepicker'
                }
            ),
            'priority': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'cycle': forms.TextInput(
                attrs={
                    'placeholder': 'Cycle',
                    'class': 'form-control'
                }
            ),
            'tags': forms.TextInput(
                attrs={
                    'placeholder': 'Tags',
                    'class': 'form-control'
                }
            ),
            'private_comment': forms.Textarea(
                attrs={
                    'placeholder': 'Private Comment',
                    'class': 'form-control',
                    'rows': 13
                }
            ),
            'board': forms.HiddenInput()
        }

    def save(self, commit=True):
        ticket = super(TicketForm, self).save(commit=False)

        if not ticket.zendesk_ticket_id:
            ticket.zendesk_ticket_id = None

        if ticket.tags is None:
            ticket.tags = ''

        if commit:
            ticket.save()

        return ticket


class TicketUpdateOnceForm(forms.Form):
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'edit_subject',
                'class': 'input',
                'placeholder': 'Subject'
            }
        ), required=False
    )
    requester = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'edit_requester',
                'class': 'input',
                'placeholder': 'Requester'
            }
        ), required=False
    )
    tags = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'edit_tags',
                'class': 'input',
                'placeholder': 'Tags'
            }
        ), required=False
    )
    due_at = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'edit_due_at',
                'type': 'input',
                'placeholder': 'mm/dd/yyyy',
                'class': 'input'
            }
        ), required=False
    )
    assignee = forms.ModelChoiceField(
        queryset=Agent.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'edit_assignee',
                'placeholder': 'Select Assignee'
            }
        ), required=False,
        empty_label='Select Assignee'
    )
