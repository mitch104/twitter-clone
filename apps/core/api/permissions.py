from rest_framework import permissions
from rest_framework_api_key.permissions import HasAPIKey


class HasAPIKeyOrIsAuthenticated(permissions.BasePermission):
    """
    Allow access if the user is authenticated or has a valid API key.
    """

    def has_permission(self, request, view):
        # Check if user is authenticated
        if request.user and request.user.is_authenticated:
            return True

        # Check if request has a valid API key
        return HasAPIKey().has_permission(request, view)
