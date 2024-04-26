from django.db import models


class Rick(models.Model):
    """
        A model for our infinite Ricks
    """
    universe = models.CharField(max_length=255, unique=True)
    is_morty_alive = models.BooleanField()
