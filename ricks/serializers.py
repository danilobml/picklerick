from rest_framework import serializers
from morties.serializers import MortySerializer
from .models import Rick
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


class RickSerializer(serializers.ModelSerializer):
    """
        Serializer for Ricks
    """

    paired_morties = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Rick
        exclude = ('user',)

    def validate_universe(self, value):
        if self.instance and self.instance.universe != value:
            raise ValidationError({"error": "You may not change a Rick's universe!"})
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = f"Rick{validated_data['universe']}"

        user = User.objects.create_user(username=username, password=password)
        validated_data['user'] = user

        return super().create(validated_data)

    def get_paired_morties(self, obj):
        user = self.context['request'].user
        if user == obj.user or user.is_staff:
            return MortySerializer(obj.paired_morties.all(), many=True).data
        return []
