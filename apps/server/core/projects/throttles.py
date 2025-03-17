"""
Throttles pour les vues de l'application projects
"""

from rest_framework.throttling import SimpleRateThrottle


class ProjectThrottle(SimpleRateThrottle):
    """
    Throttle pour les tentatives de projects
    """

    scope = "projects"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
