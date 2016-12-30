from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'comment',
        'requester',
        'requester_id',
        'assignee',
        'ticket_type',
        'priority',
        'tags',
        'sheet',
    )
    list_filter = ('sheet__name',)
