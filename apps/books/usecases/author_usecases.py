from datetime import datetime

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.books.exceptions import AuthorNotFound
from apps.books.models import Author


class AddAuthorUseCase:
    """
    To add all authors
    """

    def __init__(self, serializer):
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self.author = Author(**self._data)
        self.author.save()


class ListAuthorUseCase:
    """
    To list all authors
    """

    def execute(self):
        self._factory()
        return self.author

    def _factory(self):
        self.author = Author.objects.all()
        # self.author.save()


class GetAuthorUseCase:
    """
    get author instance
    """

    def __init__(self, author_id):
        self._author_id = author_id

    def execute(self):
        self._factory()
        return self._author

    def _factory(self):
        try:
            self._author = Author.objects.get(pk=self._author_id)
        except Author.DoesNotExist:
            raise AuthorNotFound


class UpdateAuthorUseCase:
    """
    Update authors
    """

    def __init__(self, author: Author, serializer):
        self._author = author
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            # using set attr to update each object sent from serializers
            setattr(self._author, key, self._data.get(key))
        self._author.updated_date = datetime.now()
        # Save author
        self._author.save()


class DeleteAuthorUseCase:
    def __init__(self, author: Author):
        self._author = author

    def execute(self):
        self._factory()

    def _factory(self):
        # delete author instance based on the instance we get from views.py
        self._author.delete()
