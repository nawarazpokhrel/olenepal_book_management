from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

from apps.books.exceptions import BookBorrowNotFound
from apps.books.models import BookBorrow, Book, BookReturn


class CreateBookBorrowUseCase:
    def __init__(self, book: Book, serializer):
        self._book = book
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self.book_borrow = BookBorrow(
            book=self._book,
            **self._data
        )
        try:
            self.book_borrow.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)
        self.book_borrow.save()


class GetBookBorrowUseCase:
    """
    get book borrow instance
    """

    def __init__(self, book_borrow_id):
        self._book_borrow_id = book_borrow_id

    def execute(self):
        self._factory()
        return self.book_borrow

    def _factory(self):
        try:
            self.book_borrow = BookBorrow.objects.get(pk=self._book_borrow_id)
        except BookBorrow.DoesNotExist:
            raise BookBorrowNotFound


class CreateBookReturnUseCase:
    def __init__(self, book_borrow: BookBorrow, serializer):
        self._book_borrow = book_borrow
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self.book_return = BookReturn(
            book_borrowed=self._book_borrow,
            **self._data
        )
        try:
            self.book_return.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)
        self.book_return.save()
