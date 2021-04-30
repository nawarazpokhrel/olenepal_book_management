from django.urls import path, include

from apps.books import urls

urlpatterns = [

    path(
        'author/',
        include('apps.books.urls.author_urls')
    ),
    path(
        '',
        include('apps.books.urls.book_urls')
    ),
    path(
        'publication/',
        include('apps.books.urls.publication_urls')
    ),
    path(
        '',
        include('apps.books.urls.book_borrow_urls')
    ),
]
