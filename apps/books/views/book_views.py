from apps.books.mixins import AuthorMixin
from apps.books.serializers import book_serializers
from apps.books.usecases import book_usecases
from apps.core import generics


class AddBookView(generics.CreateAPIView, AuthorMixin):
    """
    Use this to add book
    """
    serializer_class = book_serializers.AddBookSerializer

    def get_object(self):
        return self.get_author()

    def perform_create(self, serializer):
        return book_usecases.AddBookUseCase(
            author=self.get_author(),
            serializer=serializer
        ).execute()
