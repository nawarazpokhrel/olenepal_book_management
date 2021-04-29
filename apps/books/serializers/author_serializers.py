from rest_framework import serializers

from apps.books import models
from apps.books.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class AddAuthorSerializer(AuthorSerializer):
    class Meta(AuthorSerializer.Meta):
        fields = (
            'name',
            'address',
            'phone_number',
            'publication',
        )


class ListAuthorSerializer(AuthorSerializer):
    date_created = serializers.DateTimeField(format='%Y-%M-%D')

    class Meta(AuthorSerializer.Meta):
        fields = (
            'id',
            'name',
            'address',
            'phone_number',
            'publication',
            'date_created',
        )


class UpdateAuthorSerializer(AuthorSerializer):
    class Meta(AuthorSerializer.Meta):
        fields = (
            'name',
            'address',
            'phone_number',
            'publication',
        )
