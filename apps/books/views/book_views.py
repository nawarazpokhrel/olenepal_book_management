from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from apps.books import filtersets
from apps.books.mixins import AuthorMixin
from apps.books.serializers import book_serializers
from apps.books.usecases import book_usecases
from apps.core import generics


class AddBookView(generics.CreateAPIView, AuthorMixin):
    """
    Use this to add book
    """
    serializer_class = book_serializers.AddBookSerializer

    def get_object(self):
        return self.get_author()

    def perform_create(self, serializer):
        return book_usecases.AddBookUseCase(
            author=self.get_author(),
            serializer=serializer
        ).execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response('created successfully', status=status.HTTP_201_CREATED)


class ListBookView(generics.ListAPIView):
    """
    Use this to list books
    """
    serializer_class = book_serializers.ListBookSerializer
    no_content_error_message = 'No books at the moment from your search try again'
    # These are the filters used to filter book name, genre, edition etc
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['edition', 'name']
    filterset_class = filtersets.BookSearchFilter

    def get_queryset(self):
        return book_usecases.ListBookUseCase().execute()
