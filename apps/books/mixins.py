from apps.books.usecases.author_usecases import GetAuthorUseCase
from apps.books.usecases.book_usecases import GetBookUseCase


class AuthorMixin:
    def get_author(self):
        return GetAuthorUseCase(
            author_id=self.kwargs.get('author_id')
        ).execute()


class BookMixin:
    def get_book(self):
        return GetBookUseCase(
            book_id=self.kwargs.get('book_id')
        ).execute()
