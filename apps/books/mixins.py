from apps.books.usecases.author_usecases import GetAuthorUseCase
from apps.books.usecases.book_usecases import GetBookUseCase
from apps.books.usecases.publication_usecases import GetPublicationUseCase

"""
These class are usually made to get model instance of particular model
"""
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


class PublicationMixin:
    def get_publication(self):
        return GetPublicationUseCase(
            publication_id=self.kwargs.get('publication_id')
        ).execute()
