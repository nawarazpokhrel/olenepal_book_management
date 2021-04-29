from rest_framework import serializers

from apps.books.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class AddAuthorSerializer(AuthorSerializer):
    class Meta(AuthorSerializer.Meta):
        fields = (
            'user',
            'publication',
        )


class ListAuthorSerializer(AuthorSerializer):
    # Formatting date time based on first time and then date
    user = serializers.CharField()
    publication = serializers.CharField()
    date_created = serializers.DateTimeField(format='%I-%m %p %Y-%m-%d')

    class Meta(AuthorSerializer.Meta):
        fields = (
            'id',
            'user',
            'address',
            'publication',
            'date_created',
        )


class UpdateAuthorSerializer(AuthorSerializer):
    class Meta(AuthorSerializer.Meta):
        fields = (
            'user',
            'publication',
        )
