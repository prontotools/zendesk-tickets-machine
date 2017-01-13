from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'comment',
        'requester',
        'assignee',
        'ticket_type',
        'priority',
        'tags',
        'board',
    )
    list_filter = ('board__name',)
