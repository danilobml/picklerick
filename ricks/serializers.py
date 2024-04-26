from rest_framework.serializers import ModelSerializer
from .models import Rick


class RickSerializer(ModelSerializer):
    """
        Serializer for Ricks
    """
    class Meta:
        model = Rick
        fields = "__all__"
