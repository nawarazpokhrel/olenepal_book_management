from rest_framework import serializers

from apps.books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class AddBookSerializer(BookSerializer):
    class Meta(BookSerializer.Meta):
        fields = (
            'name',
            'edition',
            'available_books',
            'genre',
            # 'publication',
        )


class ListBookSerializer(BookSerializer):
    # To provide publication name instead of publication Id
    publication = serializers.ListSerializer(child=serializers.CharField())
    author = serializers.CharField()

    class Meta(BookSerializer.Meta):
        fields = (
            'id',
            'name',
            'author',
            'edition',
            'available_books',
            'genre',
            'publication',
        )


class UpdateBookSerializer(BookSerializer):
    class Meta(BookSerializer.Meta):
        fields = (
            'id',
            'name',
            'edition',
            'available_books',
            'genre',
        )


class AddBookPublicationSerializer(BookSerializer):
    """
    To add book to publication
    """
    class Meta(BookSerializer.Meta):
        fields = (
            'publication',
        )


class RemoveBookPublicationSerializer(AddBookPublicationSerializer):
    """
    To remove book from publication
    """
    pass
