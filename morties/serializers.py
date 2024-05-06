from rest_framework import serializers
from .models import Morty


class MortySerializer(serializers.ModelSerializer):
    """
        Serializer for Morties
    """

    paired_rick = serializers.StringRelatedField()

    class Meta:
        model = Morty
        fields = "__all__"
