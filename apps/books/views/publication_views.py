from rest_framework import status
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from apps.books.mixins import PublicationMixin
from apps.books.serializers import publication_serializers
from apps.books.usecases import publication_usecases
from apps.core import generics


class AddPublicationView(generics.CreateAPIView):
    """
    Use this endpoint to add publication
    """
    serializer_class = publication_serializers.AddPublicationSerializer

    def perform_create(self, serializer):
        return publication_usecases.AddPublicationUseCase(serializer=serializer).execute()

    def response(self, serializer, result, status_code):
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'created': 'Publication created successfully'},
            status=status.HTTP_201_CREATED, headers=headers
        )


class ListPublicationView(generics.ListAPIView):
    """
    Use this endpoint to get  list of publications
    """
    serializer_class = publication_serializers.ListPublicationSerializer
    no_content_error_message = 'No publication At the moment'

    def get_queryset(self):
        return publication_usecases.ListPublicationUseCase().execute()


class UpdatePublicationView(UpdateAPIView, PublicationMixin):
    """
    Use this endpoint to update author
    """
    serializer_class = publication_serializers.UpdatePublicationSerializer

    def get_object(self):
        return self.get_publication()

    def perform_update(self, serializer):
        return publication_usecases.UpdatePublicationUseCase(
            publication=self.get_publication(),
            serializer=serializer
        ).execute()


class DeletePublicationView(DestroyAPIView, PublicationMixin):
    """
    Use this endpoint to delete publication
    """

    def get_object(self):
        return self.get_publication()

    def perform_destroy(self, instance):
        return publication_usecases.DeletePublicationUseCase(
            publication=self.get_publication(),
        ).execute()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'deleted': 'Publication was deleted.'},
            status=status.HTTP_204_NO_CONTENT
        )
