from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin


class BaseModelAdmin(ModelAdmin):
    list_display = (
        'id',
        'updated_at',
    )
    list_display_links = (
        'id',
    )
    search_fields = (
        'id',
    )
    ordering = (
        '-created_at',
    )
    list_per_page = (
        25
    )