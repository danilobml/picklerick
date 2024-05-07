from django.db import models
from morties.models import Morty


class Rick(models.Model):
    """
        A model for our infinite Ricks
    """
    universe = models.CharField(max_length=255, unique=True)
    paired_morty = models.OneToOneField(Morty,
                                        on_delete=models.PROTECT,
                                        related_name='paired_rick',
                                        null=True,
                                        blank=True)
