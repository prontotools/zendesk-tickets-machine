from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'requester',
        'assignee',
        'ticket_type',
        'priority',
        'tags',
    )
