from django.urls import path, include

from apps.books import urls

urlpatterns = [

    path('author/', include('apps.books.urls.author_urls')),
]
