from django.utils.translation import gettext_lazy as _
from rest_framework import status

from rest_framework.exceptions import NotFound


class AuthorNotFound(NotFound):
    default_detail = _('Author not found for given Id.')


class BookNotFound(NotFound):
    default_detail = _('Book not found for given Id.')


class PublicationNotFound(NotFound):
    default_detail = _('Publication not found for given Id.')


class BookBorrowNotFound(NotFound):
    default_detail = _('Book Borrow not found for given Id.')
