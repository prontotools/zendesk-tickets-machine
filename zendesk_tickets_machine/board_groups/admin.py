from django.contrib import admin

from .models import BoardGroup


@admin.register(BoardGroup)
class BoardGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
