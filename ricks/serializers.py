from rest_framework import serializers
from morties.serializers import MortySerializer
from .models import Rick


class RickSerializer(serializers.ModelSerializer):
    """
        Serializer for Ricks
    """

    paired_morties = MortySerializer(many=True, read_only=True)

    class Meta:
        model = Rick
        fields = "__all__"
