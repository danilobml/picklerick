from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Morty


class MortySerializer(serializers.ModelSerializer):
    """
    Serializer for Morties
    """

    class Meta:
        model = Morty
        fields = "__all__"

    def validate_paired_rick(self, rick):
        if rick is None:
            return None
        if rick.paired_morties.filter(is_alive=True).exists() and self.initial_data.get("is_alive"):
            raise ValidationError({"error": "Rick already has a living paired Morty."})
        return rick
