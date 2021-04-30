from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users import views

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

    path(
        'login',
        TokenObtainPairView.as_view(),
        name='login'
    ),
    path(
        'login/refresh',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
