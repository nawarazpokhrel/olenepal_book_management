from rest_framework import generics, status
from rest_framework.response import Response

from apps.books.mixins import AuthorMixin
from apps.books.usecases import author_usecases
from apps.books.serializers import author_serializers


class AddAuthorViews(generics.CreateAPIView):
    serializer_class = author_serializers.AddAuthorSerializer

    def perform_create(self, serializer):
        return author_usecases.AddAuthorUseCase(serializer=serializer).execute()


class ListAuthorViews(generics.ListAPIView):
    serializer_class = author_serializers.ListAuthorSerializer

    def get_queryset(self):
        return author_usecases.ListAuthorUseCase().execute()


class UpdateAuthorViews(generics.UpdateAPIView, AuthorMixin):
    serializer_class = author_serializers.UpdateAuthorSerializer

    def get_object(self):
        return self.get_author()

    def perform_update(self, serializer):
        return author_usecases.UpdateAuthorUseCase(
            author=self.get_author(),
            serializer=serializer
        ).execute()


class DeleteAuthorViews(generics.DestroyAPIView, AuthorMixin):

    def get_object(self):
        return self.get_author()

    def perform_destroy(self, instance):
        return author_usecases.DeleteAuthorUseCase(
            author=self.get_author(),
        ).execute()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'deleted': 'Author was deleted.'}, status=status.HTTP_204_NO_CONTENT)
