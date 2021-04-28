import jwt
from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()
# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.generics import CreateAPIView
from olenepal_book_management.settings import SECRET_KEY
from users import serializers, usecases
from users.mixins import ResponseMixin


class RegisterUserView(CreateAPIView, ResponseMixin):
    """
    Use this to register user
    """
    serializer_class = serializers.RegisterUserSerializer
    permission_classes = (AllowAny,)
    response_serializer_class = serializers.RegisterUserResponseSerializer

    def perform_create(self, serializer):
        return usecases.RegisterUserUseCase(
            serializer=serializer,
            request=self.request
        ).execute()

    def response(self, serializer, result, status_code):
        serializer = self.get_response_serializer(result)
        return Response(serializer.data, status=status_code)

    # This decorator was added since drf swagger does not give default response in swagger
    @swagger_auto_schema(responses={200: serializers.RegisterUserResponseSerializer()})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VerifyEmailView(generics.GenericAPIView):
    """
    Use this to verify user email
    """

    def get(self, request):
        # First get token from user browser
        token = request.GET.get('token')
        try:
            # decoding the token along with secret key
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
            # get the user that sent the payload
            user = User.objects.get(id=payload['user_id'])
            # now verify the user
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        # raise exceptions if token expired
        except jwt.ExpiredSignatureError as e:
            return Response({'error': 'Activations link expired'}, status=status.HTTP_400_BAD_REQUEST)
        # raise exception if the token sent is wrong
        except jwt.exceptions.DecodeError as e:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
