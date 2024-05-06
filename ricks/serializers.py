from rest_framework import serializers
from .models import Rick


class RickSerializer(serializers.ModelSerializer):
    """
        Serializer for Ricks
    """
    paired_morty_universe = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rick
        fields = "__all__"

    def get_paired_morty_universe(self, rick_instance):
        if rick_instance.paired_morty is not None:
            return rick_instance.paired_morty.universe
        return None
