"""
Throttles pour les vues de l'application stack
"""

from rest_framework.throttling import SimpleRateThrottle


class StacksThrottle(SimpleRateThrottle):
    """
    Throttle pour les tentatives de stack
    """

    scope = "stack"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
