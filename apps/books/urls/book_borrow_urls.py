from django.urls import path

from apps.books.views import book_borrow_views

urlpatterns = [
    path(
        '<str:book_id>/book-borrow/create',
        book_borrow_views.CreateBookBorrowView.as_view(),
        name='create-book-borrow'
    ),
    path(
        'book-borrow/<str:book_borrow_id>/book-return/create',
        book_borrow_views.CreateBookReturnView.as_view(),
        name='create-book-return'
    )

]
