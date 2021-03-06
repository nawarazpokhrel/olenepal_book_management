from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from apps.books import filtersets
from apps.books.mixins import AuthorMixin, BookMixin
from apps.users.permissions import IsOwnBook, IsLibrarianUser
from apps.books.serializers import book_serializers
from apps.books.usecases import book_usecases
from apps.core import generics
from apps.users.permissions import IsAuthorUser


class AddBookView(generics.CreateAPIView, AuthorMixin):
    """
    Use this to add book
    """
    serializer_class = book_serializers.AddBookSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        obj = self.get_author()
        self.check_object_permissions(self.request, obj)
        return self.get_author()

    def perform_create(self, serializer):
        return book_usecases.AddBookUseCase(
            author=self.get_object(),
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
    filter_backends = (DjangoFilterBackend,)
    # ordering_fields = ['edition', 'name']
    filterset_class = filtersets.BookSearchFilter
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return book_usecases.ListBookUseCase().execute()


class AddBookPublicationView(generics.CreateAPIView, BookMixin):
    serializer_class = book_serializers.AddBookPublicationSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self):
        return self.get_book()

    def perform_create(self, serializer):
        return book_usecases.AddBookPublicationUseCase(
            serializer=serializer,
            book=self.get_book(),
        ).execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response('Publication Added successfully to book', status=status.HTTP_201_CREATED)


class RemoveBookPublicationView(generics.CreateAPIView, BookMixin):
    serializer_class = book_serializers.RemoveBookPublicationSerializer

    permission_classes = (IsAdminUser,)

    def get_object(self):
        return self.get_book()

    def perform_create(self, serializer):
        return book_usecases.RemoveBookPublicationUseCase(
            serializer=serializer,
            book=self.get_book(),
        ).execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response('Publication removed successfully from book', status=status.HTTP_201_CREATED)


class DeleteBookView(DestroyAPIView, BookMixin):
    """
    Use this to delete book
    """

    permission_classes = (IsAdminUser, IsAuthorUser, IsOwnBook,)

    def get_object(self):
        return self.get_book()

    def perform_destroy(self, instance):
        return book_usecases.DeleteBookUseCase(
            book=self.get_object()
        ).execute()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'deleted': 'Book deleted'}, status=status.HTTP_204_NO_CONTENT)


class UpdateBookView(UpdateAPIView, BookMixin):
    """
    Use this to update book
    """

    serializer_class = book_serializers.UpdateBookSerializer

    permission_classes = (IsOwnBook, IsAdminUser, IsLibrarianUser,)

    def get_object(self):
        obj = self.get_book()
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        return book_usecases.UpdateBookUseCase(
            book=self.get_object(),
            serializer=serializer
        ).execute()
