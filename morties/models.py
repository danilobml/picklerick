from django.db import models


class Morty(models.Model):
    """
        A Model for the Morties (because they are a person too)
    """
    universe = models.CharField(max_length=255, unique=True)
    is_alive = models.BooleanField(default=True, blank=True)
    paired_rick = models.ForeignKey('ricks.Rick',
                                    on_delete=models.PROTECT, related_name="paired_morties",
                                    null=True, blank=True, default=None)
