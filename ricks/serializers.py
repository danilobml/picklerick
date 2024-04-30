from rest_framework import serializers
from .models import Rick


class RickSerializer(serializers.ModelSerializer):
    """
        Serializer for Ricks
    """
    paired_morty_universe = serializers.SerializerMethodField()

    class Meta:
        model = Rick
        fields = "__all__"

    def get_paired_morty_universe(self, rick_instance):
        try:
            if rick_instance.paired_morty:
                return rick_instance.paired_morty.universe
        except Exception:
            return ""
