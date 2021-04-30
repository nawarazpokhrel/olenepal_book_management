from rest_framework import serializers

from apps.books.models import Publication


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = "__all__"


class AddPublicationSerializer(PublicationSerializer):
    class Meta(PublicationSerializer.Meta):
        fields = (
            'name',
            'address',
            'phone_number',
        )


class ListPublicationSerializer(PublicationSerializer):
    class Meta(PublicationSerializer.Meta):
        fields = (
            'id',
            'name',
            'address',
            'phone_number',
        )


class UpdatePublicationSerializer(PublicationSerializer):
    class Meta(PublicationSerializer.Meta):
        fields = (
            'name',
            'address',
            'phone_number',
        )
