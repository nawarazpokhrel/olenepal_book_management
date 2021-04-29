from rest_framework import serializers

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
    # Formatting date time based on first time and then date
    date_created = serializers.DateTimeField(format='%I-%m %p %Y-%m-%d')

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
