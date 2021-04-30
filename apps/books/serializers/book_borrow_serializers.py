from rest_framework import serializers

from apps.books.models import BookBorrow, BookReturn


class BookBorrowSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookBorrow
        fields = '__all__'


class CreateBookBorrowSerializer(BookBorrowSerializers):
    class Meta(BookBorrowSerializers.Meta):
        fields = (
            'user',
            'date_borrowed',
            'return_date',
        )


class CreateBookReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReturn
        fields = (
            'returned_date',
        )
