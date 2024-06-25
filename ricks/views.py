from rest_framework.viewsets import ModelViewSet
from .models import Rick
from .serializers import RickSerializer


class RickViewSet(ModelViewSet):
    """
        A viewset for viewing and editing Rick(s).
    """

    serializer_class = RickSerializer
    queryset = Rick.objects.all()
