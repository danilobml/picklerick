from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Morty
from ricks.models import Rick


class MortySerializer(serializers.ModelSerializer):
    """
    Serializer for Morties
    """

    class Meta:
        model = Morty
        fields = "__all__"

    def validate(self, data):
        rick = data.get('paired_rick')
        if rick is None:
            return data

        rick = Rick.objects.get(pk=rick.id)
        if rick.paired_morties.filter(is_alive=True).exists() and data.get("is_alive"):
            raise ValidationError({"error": "Rick already has a living paired Morty."})

        return data
