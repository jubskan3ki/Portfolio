"""
Throttles pour les vues de l'application experience.
"""

from rest_framework.throttling import SimpleRateThrottle


class ExperienceThrottle(SimpleRateThrottle):
    """
    Throttle pour les tentatives sur Experience.
    """

    scope = "experience"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
