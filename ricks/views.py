from rest_framework.viewsets import ModelViewSet
from .models import Rick
from .serializers import RickSerializer
from rest_framework.permissions import IsAdminUser
from picklerick.permissions import IsUserAuthenticatedRick


class RickViewSet(ModelViewSet):
    """
        A viewset for viewing and editing Rick(s).
    """
    permission_classes = (IsAdminUser | IsUserAuthenticatedRick, )

    serializer_class = RickSerializer
    queryset = Rick.objects.all()
