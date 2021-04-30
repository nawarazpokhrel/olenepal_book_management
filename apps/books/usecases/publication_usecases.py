from datetime import datetime

from apps.books.exceptions import PublicationNotFound
from apps.books.models import Publication


class AddPublicationUseCase:
    """
    To add  publication
    """

    def __init__(self, serializer):
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self.publication = Publication(**self._data)
        self.publication.save()


class ListPublicationUseCase:
    """
    Use this to list publications
    """

    def execute(self):
        self._factory()
        return self.publications

    def _factory(self):
        self.publications = Publication.objects.all()


class GetPublicationUseCase:
    """
    get publication instance
    """

    def __init__(self, publication_id):
        self._publication_id = publication_id

    def execute(self):
        self._factory()
        return self._publication

    def _factory(self):
        try:
            self._publication = Publication.objects.get(pk=self._publication_id)
        except Publication.DoesNotExist:
            raise PublicationNotFound


class UpdatePublicationUseCase:
    """
    Update publication
    """

    def __init__(self, publication: Publication, serializer):
        self._publication = publication
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            # using set attr to update each object sent from serializers
            setattr(self._publication, key, self._data.get(key))
        self._publication.updated_date = datetime.now()
        # Save publication
        self._publication.save()


class DeletePublicationUseCase:
    def __init__(self, publication: Publication):
        self._publication = publication

    def execute(self):
        self._factory()

    def _factory(self):
        # delete author instance based on the instance we get from views.py
        self._publication.delete()
