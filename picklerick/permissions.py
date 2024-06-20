from rest_framework import permissions
from ricks.models import Rick


class IsUserAuthenticatedRick(permissions.BasePermission):
    """
        Custom permission to allow only authenticated ricks to view data
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return Rick.objects.filter(user=request.user).exists()
