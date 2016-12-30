from django.contrib import admin

from .models import Sheet

class SheetAdmin(admin.ModelAdmin):
	list_display = {
		'name',
		'slug',
	}
