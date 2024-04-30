from django.db import models
from ricks.models import Rick


class Morty(models.Model):
    """
        A Model for the Morties (because they are a person too)
    """
    universe = models.CharField(max_length=255, unique=True)
    is_alive = models.BooleanField(default=True)
    paired_rick = models.OneToOneField(Rick, on_delete=models.PROTECT)
