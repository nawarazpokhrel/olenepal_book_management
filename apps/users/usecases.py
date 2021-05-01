from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core import utils
from apps.core.utils import SendEmail
from apps.users.exceptions import UserNotFound
# from olenepal_book_management.tasks import  email

User = get_user_model()


class RegisterUserUseCase:
    """
    endpoint to register users
    """

    def __init__(self, serializer, request):
        self.serializer = serializer
        self._data = serializer.validated_data
        self._request = request

    def execute(self):
        self._factory()
        return self._result

    def _factory(self):
        password = self._data.pop('password')
        self._user = User(**self._data)
        self._user.set_password(password)
        self._user.save()
        try:
            # Get user
            user_instance = User.objects.get(
                id=self._user.id,
                email=self._data['email'],
                is_active=True
            )
        except User.DoesNotExist:
            raise ValidationError('User does not exists')
        token = RefreshToken.for_user(user=user_instance).access_token
        # get current site
        current_site = get_current_site(self._request).domain
        # we are calling verify by email view  here whose name path is activate-by-email
        relative_link = reverse('activate-by-email')
        # make whole url
        absolute_url = 'http://' + current_site + relative_link + "?token=" + str(token)
        # write email body
        email_body = 'Welcome ' + user_instance.username + \
                     " Use link below to verify your " \
                     "email " + absolute_url

        data = {
            'email_body': email_body,
            'email_subject': 'Verify email',
            'to_email': user_instance.email
        }
        # call send email function
        SendEmail.email(data)
        self._result = {
            'user': self._user
        }


class ListUserUseCase:
    def execute(self):
        self._factory()
        return self._user

    def _factory(self):
        self._user = User.objects.all()


class ListVerifiedUserUseCase:
    def execute(self):
        self._factory()
        return self._user

    def _factory(self):
        self._user = User.objects.filter(is_verified=True)


class GetUserUseCase:
    """
    get user instance
    """

    def __init__(self, user_id):
        self._user_id = user_id

    def execute(self):
        self._factory()
        return self._user

    def _factory(self):
        try:
            self._user = User.objects.get(pk=self._user_id)
        except User.DoesNotExist:
            raise UserNotFound
