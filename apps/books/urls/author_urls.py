from django.urls import path, include

from apps.books.views import author_views

urlpatterns = [
    path(
        'add',
        author_views.AddAuthorViews.as_view(),
        name='Add-authors'
    ),
    path(
        'list',
        author_views.ListAuthorViews.as_view(),
        name='List-authors'
    ),
    path(
        '<str:author_id>/update',
        author_views.UpdateAuthorViews.as_view(),
        name='update-authors'
    ),
    path(
        '<str:author_id>/delete',
        author_views.DeleteAuthorViews.as_view(),
        name='delete-authors'
    ),
]
