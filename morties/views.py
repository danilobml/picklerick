from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import Morty
from .serializers import MortySerializer
from ricks.models import Rick
from rest_framework.response import Response
from rest_framework import status


class MortyViewSet(ModelViewSet):
    """
        A viewset for Morties.
    """
    serializer_class = MortySerializer
    queryset = Morty.objects.all()

    def perform_create(self, serializer):
        if self.has_no_alive_morties():
            serializer.save()

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        if self.has_no_alive_morties():
            serializer.save()

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def has_no_alive_morties(self):
        rick_id = self.request.data.get('paired_rick')
        if rick_id is None:
            return True
        rick = get_object_or_404(Rick, pk=rick_id)
        if rick.paired_morties.filter(is_alive=True).exists() and self.request.data.get("is_alive"):
            raise ValidationError({"error": "Rick already has a living paired Morty."})
        return True
