from django.urls import path

from users import views

urlpatterns = [
    path(
        'register',
        views.RegisterUserView.as_view()
    ),
    path(
        'activate-by-email',
        views.VerifyEmailView.as_view(),
        name='activate-by-email'
    ),
    path(
        'list',
        views.ListUserView.as_view(),
        name='list-all-users'
    ),
    path(
        'list/verified',
        views.ListVerifiedUserView.as_view(),
        name='list-verified-users'
    ),
]
