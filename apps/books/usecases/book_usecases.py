from datetime import datetime

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
