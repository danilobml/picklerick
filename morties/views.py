
from rest_framework.viewsets import ModelViewSet
from .models import Morty
from .serializers import MortySerializer


class MortyViewSet(ModelViewSet):
    """
        A viewset for Morties.
    """
    serializer_class = MortySerializer
    queryset = Morty.objects.all()
