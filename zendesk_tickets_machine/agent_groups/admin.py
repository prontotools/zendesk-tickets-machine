from django.contrib import admin

from .models import AgentGroup


@admin.register(AgentGroup)
class AgentGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'zendesk_group_id',
    )
