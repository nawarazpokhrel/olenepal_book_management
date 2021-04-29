from django_filters import rest_framework as filters

from apps.books.models import Book


class BookSearchFilter(filters.FilterSet):
    name = filters.CharFilter(
        label='book name'
    )
    author = filters.CharFilter(
        label='book author'
    )
    publication = filters.CharFilter(
        label='book publication'
    )
    edition = filters.CharFilter(
        label='book edition'
    )
    genre = filters.CharFilter(
        label='book genre'
    )

    class Meta:
        model = Book
        fields = (
            'name',
            'author',
            'publication',
            'edition',
            'genre',
        )
