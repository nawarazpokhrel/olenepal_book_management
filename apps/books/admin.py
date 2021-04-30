from django.contrib import admin

# Register your models here.
from apps.books import models
from apps.core.admin import BaseModelAdmin


@admin.register(models.Publication)
class PublicationAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'name',
        'address',
        'phone_number'
    )

    list_display_links = ('name',)

    list_filter = ('name',)


@admin.register(models.Author)
class AuthorAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'user',
        'address',
    )

    list_display_links = ('id',)

    list_filter = (
        'user',
        'publication',
    )


@admin.register(models.Book)
class BookAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'name',
        'author',
        'edition',
    )

    list_display_links = ('name',)

    list_filter = (
        'name',
        'author',
        'publication',
        'edition',
    )


@admin.register(models.BookBorrow)
class BookBorrowAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'book',
        'user',
        'date_borrowed',
    )

    list_display_links = ('book',)

    list_filter = (
        'book',
        'user',
    )
    readonly_fields = ('number_of_days_issued',)


@admin.register(models.BookReturn)
class BookReturnAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'book_borrowed',
        'returned_date',
        'actual_issued_days',
    )

    list_display_links = ('book_borrowed',)

    list_filter = (
        'book_borrowed__book',
    )
    readonly_fields = ('actual_issued_days', 'fine_amount',)
