from django.db import models
from morties.serializers import MortySerializer


class Rick(models.Model):
    """
        A model for our infinite Ricks
    """
    paired_morties = MortySerializer(many=True)
    universe = models.CharField(max_length=255, unique=True)
