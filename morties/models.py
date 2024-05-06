from django.db import models


class Morty(models.Model):
    """
        A Model for the Morties (because they are a person too)
    """
    universe = models.CharField(max_length=255, unique=True)
    is_alive = models.BooleanField(default=True, blank=True)
