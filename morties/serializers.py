from rest_framework.serializers import ModelSerializer
from .models import Morty


class MortySerializer(ModelSerializer):
    """
        Serializer for Morties
    """
    class Meta:
        model = Morty
        fields = "__all__"
