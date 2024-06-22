from rest_framework import serializers
from morties.serializers import MortySerializer
from .models import Rick
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


class RickSerializer(serializers.ModelSerializer):
    """
        Serializer for Ricks
    """

    paired_morties = MortySerializer(many=True, read_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Rick
        fields = "__all__"
        read_only_fields = ['user']

    def validate_universe(self, value):
        if self.instance and self.instance.universe != value:
            raise ValidationError({"error": "You may not change a Rick's universe!"})
        return value

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = User.objects.create_user(username=username, password=password)
        validated_data['user'] = user

        return super().create(validated_data)
