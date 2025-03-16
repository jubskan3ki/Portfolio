"""
Throttles pour les vues de l'application user
"""

from rest_framework.throttling import SimpleRateThrottle


class LoginThrottle(SimpleRateThrottle):
    """
    Throttle pour les tentatives de login
    """

    scope = "login"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class ResetPasswordThrottle(SimpleRateThrottle):
    """
    Throttle pour les demandes de reset de mot de passe
    """

    scope = "reset_password"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
