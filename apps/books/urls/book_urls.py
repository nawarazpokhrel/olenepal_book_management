from django.urls import path

from apps.books.views import book_views

urlpatterns = [
    path(
        'author/<str:author_id>/add',
        book_views.AddBookView.as_view(),
        name='Add-book'
    ),
    path(
        'list',
        book_views.ListBookView.as_view(),
        name='List-book'
    ),
]
