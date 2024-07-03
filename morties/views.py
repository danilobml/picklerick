from rest_framework.viewsets import ModelViewSet
from .models import Morty
from .serializers import MortySerializer


class MortyViewSet(ModelViewSet):
    """
        A viewset for Morties.
    """

    serializer_class = MortySerializer
    queryset = Morty.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Morty.objects.all()
        return Morty.objects.filter(paired_rick__user=user)
