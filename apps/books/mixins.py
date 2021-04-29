from apps.books.usecases.author_usecases import GetAuthorUseCase


class AuthorMixin:
    def get_author(self):
        return GetAuthorUseCase(
            author_id=self.kwargs.get('author_id')
        ).execute()
