from rest_framework import serializers
from morties.serializers import MortySerializer
from .models import Rick
from rest_framework.exceptions import ValidationError


class RickSerializer(serializers.ModelSerializer):
    """
        Serializer for Ricks
    """

    paired_morties = MortySerializer(many=True, read_only=True)

    class Meta:
        model = Rick
        fields = "__all__"

    def validate_universe(self, value):
        if self.instance and self.instance.universe != value:
            raise ValidationError({"error": "You may not change a Rick's universe!"})
        return value
