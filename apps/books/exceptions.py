from django.utils.translation import gettext_lazy as _
from rest_framework import status

from rest_framework.exceptions import NotFound, APIException


class AuthorNotFound(NotFound):
    default_detail = _('Author not found for given Id.')

