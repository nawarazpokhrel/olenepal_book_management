from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.books.exceptions import BookNotFound
from apps.books.models import Author, Book


class AddBookUseCase:
    def __init__(self, author: Author, serializer):
        self._author = author
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self.book = Book(**self._data, author=self._author)
        self.book.save()


class ListBookUseCase:
    def execute(self):
        self._factory()
        return self.book

    def _factory(self):
        self.book = Book.objects.all()


class GetBookUseCase:
    """
    get author instance
    """

    def __init__(self, book_id):
        self._book_id = book_id

    def execute(self):
        self._factory()
        return self._book

    def _factory(self):
        try:
            self._book = Book.objects.get(pk=self._book_id)
        except Book.DoesNotExist:
            raise BookNotFound


class AddBookPublicationUseCase:
    def __init__(self, serializer, book: Book):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._book = book

    def execute(self):
        # calling is valid first so as to make sure we are send valid data to be save
        self.is_valid()
        self._factory()

    def _factory(self):
        # adding publication to book
        self._book.publication.add(*self._data.get('publication'))
        # self._book.save()

    def is_valid(self):
        # Rule 1,
        # We are not allowing publication to be added if it is already added to book before
        publication = self._book.publication.all()
        if set(self._data.get('publication')).issubset(set(publication)):
            raise ValidationError({
                'publication': _('Publication is already associated with book')
            }
            )


class RemoveBookPublicationUseCase:
    def __init__(self, serializer, book: Book):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._book = book

    def execute(self):
        # calling is valid first so as to make sure we are send valid data to be save
        self._is_valid()
        self._factory()

    def _factory(self):
        # removing publication from book
        self._book.publication.remove(*self._data.get('publication'))

    def _is_valid(self):
        publication = self._book.publication.all()
        if not set(self._data.get('publication')).issubset(set(publication)):
            raise ValidationError({
                'publication': _('Publication is not associated with book')
            }
            )


class DeleteBookUseCase:
    def __init__(self, book: Book):
        self._book = book

    def execute(self):
        self._factory()

    def _factory(self):
        # delete book instance based on the instance we get from views.py
        self._book.delete()
