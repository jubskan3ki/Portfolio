"""
Permissions personnalisées pour les vues de l'API.
"""

from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Permission personnalisée : seul le créateur peut modifier, les autres en lecture seule.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj.author == request.user
