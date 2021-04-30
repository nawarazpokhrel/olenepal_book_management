from rest_framework.permissions import IsAdminUser

from apps.books.mixins import BookMixin, BookBorrowMixin
from apps.books.serializers import book_borrow_serializers
from apps.books.usecases import book_borrow_usecases
from apps.core import generics


class CreateBookBorrowView(generics.CreateAPIView, BookMixin):
    """
    Use this to create book borrow
    """
    serializer_class = book_borrow_serializers.CreateBookBorrowSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self):
        return self.get_book()

    def perform_create(self, serializer):
        return book_borrow_usecases.CreateBookBorrowUseCase(
            book=self.get_object(),
            serializer=serializer
        ).execute()


class CreateBookReturnView(generics.CreateAPIView, BookBorrowMixin):
    """
    Use this to create book return
    """
    serializer_class = book_borrow_serializers.CreateBookReturnSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self):
        return self.get_book_borrow()

    def perform_create(self, serializer):
        return book_borrow_usecases.CreateBookReturnUseCase(
            book_borrow=self.get_object(),
            serializer=serializer
        ).execute()
