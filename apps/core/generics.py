from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.response import Response

from apps.core.exceptions import NoContent


class CreateAPIView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.perform_create(serializer)
        return self.response(serializer=serializer, result=result, status_code=status.HTTP_201_CREATED)

    def response(self, serializer, result, status_code):
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status_code, headers=headers)


class ListAPIView(generics.ListAPIView):
    no_content_error_message = _('No Content At The Moment.')

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        if len(queryset) > 0:
            return self.custom_queryset(queryset)
        raise NoContent(self.no_content_error_message)

    def custom_queryset(self, queryset):
        return queryset
