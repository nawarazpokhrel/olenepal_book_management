from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin


class BaseModelAdmin(ModelAdmin):
    list_display = (
        'id',
        'updated_date',
    )
    list_display_links = (
        'id',
    )
    search_fields = (
        'id',
    )
    ordering = (
        '-date_created',
    )
    list_per_page = (
        25
    )