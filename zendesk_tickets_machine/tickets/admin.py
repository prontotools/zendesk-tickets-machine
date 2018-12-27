from django.contrib import admin

from import_export import resources
from import_export.admin import ExportMixin

from .models import (
    Ticket,
    TicketZendeskAPIUsage
)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'comment',
        'organization',
        'requester',
        'assignee',
        'ticket_type',
        'due_at',
        'priority',
        'tags',
        'board',
        'is_active',
    )
    list_filter = (
        'board__name',
        'is_active',
    )


class TicketZendeskAPIUsageResource(resources.ModelResource):
    class Meta:
        model = TicketZendeskAPIUsage
        fields = (
            'id',
            'ticket_type',
            'priority',
            'assignee__name',
            'board__name',
            'created',
        )
        export_order = fields


@admin.register(TicketZendeskAPIUsage)
class TicketZendeskAPIUsageAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        'assignee',
        'organization',
        'requester',
        'ticket_type',
        'priority',
        'board',
        'created',
    )
    resource_class = TicketZendeskAPIUsageResource
