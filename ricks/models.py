from django.db import models
from django.contrib.auth.models import User


class Rick(models.Model):
    """
        A model for our infinite Ricks
    """
    universe = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rick', null=True, blank=True)
