from datetime import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.books.email import ConfirmationEmail, BookUpdateEmail, BookDeletedEmail, BookCreatedEmail
from apps.books.exceptions import BookNotFound
from apps.books.models import Author, Book
from apps.core import utils


class AddBookUseCase:
    def __init__(self, author: Author, serializer):
        self._author = author
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()
        self._send_email()

    def _factory(self):
        self.book = Book(**self._data, author=self._author)
        self.book.save()

    def _send_email(self):
        context = {
            'user': self.book.author.user.username,
            'book_name': self.book.name,
            'created_at': self.book.date_created
        }
        BookCreatedEmail(context=context).send(to=[self.book.author.user.email])


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


class UpdateBookUseCase:
    """
    Update authors
    """

    def __init__(self, book: Book, serializer):
        self._book = book
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()
        self._send_email()

    def _factory(self):
        self.old_book = self._book.name
        for key in self._data.keys():
            # using set attr to update each object sent from serializers
            setattr(self._book, key, self._data.get(key))
        self._book.updated_date = datetime.now()
        # Save book
        self._book.save()

    def _send_email(self):
        context = {
            'user': self._book.author.user.username,
            'new_book_name': self._book.name,
            'old_book_name': self.old_book,
            'updated_time': self._book.updated_date
        }
        BookUpdateEmail(context=context).send(to=[self._book.author.user.email])


class DeleteBookUseCase:
    """
    To delete books
    """

    def __init__(self, book: Book):
        self._book = book

    def execute(self):
        self._factory()
        self._send_email()

    def _factory(self):
        # delete book instance based on the instance we get from views.py
        book_name = self._book.name
        author_name = self._book.author.user.username
        self._book.delete()
        self.time_deleted = datetime.now()
        # call send email function

    def _send_email(self):
        context = {
            'user': self._book.author.user.username,
            'book_name': self._book.name,
            'deleted_time': self.time_deleted
        }
        BookDeletedEmail(context=context).send(to=[self._book.author.user.email])
