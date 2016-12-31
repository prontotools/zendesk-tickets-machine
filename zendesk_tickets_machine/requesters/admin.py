from django.contrib import admin

from .models import Requester


@admin.register(Requester)
class RequesterAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'zendesk_user_id',
    )
