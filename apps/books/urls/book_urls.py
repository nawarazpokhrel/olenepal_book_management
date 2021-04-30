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
    path(
        '<str:book_id>/publication/add',
        book_views.AddBookPublicationView.as_view(),
        name='add-publication-to-book'
    ),
    path(
        '<str:book_id>/publication/remove',
        book_views.RemoveBookPublicationView.as_view(),
        name='remove-publication-to-book'
    ),
    path(
        '<str:book_id>/delete',
        book_views.DeleteBookView.as_view(),
        name='delete-book'
    ),
    path(
        '<str:book_id>/update',
        book_views.UpdateBookView.as_view(),
        name='update-book'
    ),
]
