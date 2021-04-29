from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class NoContent(APIException):
    status_code = status.HTTP_204_NO_CONTENT
    default_detail = _('Content temporarily unavailable, try again later.')
    default_code = 'no content'
