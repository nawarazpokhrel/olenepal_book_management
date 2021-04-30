from django.urls import path

from apps.books.views import publication_views

urlpatterns = [
    path(
        'add',
        publication_views.AddPublicationView.as_view(),
        name='Add publication'

    ),
    path(
        'list',
        publication_views.ListPublicationView.as_view(),
        name='list-publication'
    ),

    path(
        '<str:publication_id>/update',
        publication_views.UpdatePublicationView.as_view(),
        name='update-publication'
    ),
    path(
        '<str:publication_id>/delete',
        publication_views.DeletePublicationView.as_view(),
        name='delete-publication'
    ),
]
