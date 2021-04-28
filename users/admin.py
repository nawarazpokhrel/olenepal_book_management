from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users import models
from users.models import User


class BaseUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'fullname',
        'phone_number'
    )
    search_fields = (
        'id',
        'email',
        'phone_number'
    )
    list_display_links = ('id',)

    list_filter = (
        'is_active',
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number',  'password1', 'password2'),
        }),
    )
    ordering = ('-date_joined',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'email',
            'phone_number',
            'fullname',
        )}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_librarian',
                'is_verified',
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


# Library user admin
@admin.register(models.LibraryUser)
class LibraryUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'email',
            'phone_number',
            'full_name',
        )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_librarian', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


# Normal user
@admin.register(models.NormalUser)
class NormalUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'email',
            'phone_number',
            'full_name',
        )}),
        (_('Permissions'), {
            'fields': ('is_active', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


# Admin user
@admin.register(models.AdminUser)
class AdminUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'email',
            'phone_number',
            'full_name',
        )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
