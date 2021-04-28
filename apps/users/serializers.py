from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'username',
            'email',
            'password',
            'fullname',
            'phone_number',
        )

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    default_error_messages = {
        'duplicate_phone_number': _('Phone number already exists.')
    }

    def validate_phone_number(self, value):
        if value:
            if User.objects.filter(phone_number=value).exists():
                self.fail('duplicate_phone_number')
            else:
                return value
        return value


class RegisterUserResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(source='user.id')
    username = serializers.CharField(source='user.username')


class ListUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'id',
            'username',
            'email',
            'fullname',
            'phone_number',
            'is_verified',
            'is_librarian',
            'is_active',
            'is_superuser',
        )


class ListVerifiedUserSerializer(ListUserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'id',
            'username',
            'email',
            'fullname',
            'phone_number',
            'is_librarian',
        )

