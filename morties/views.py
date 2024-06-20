
from rest_framework.viewsets import ModelViewSet
from .models import Morty
from .serializers import MortySerializer
from rest_framework.permissions import IsAdminUser
from picklerick.permissions import IsUserAuthenticatedRick


class MortyViewSet(ModelViewSet):
    """
        A viewset for Morties.
    """
    permission_classes = (IsAdminUser | IsUserAuthenticatedRick, )

    serializer_class = MortySerializer
    queryset = Morty.objects.all()
