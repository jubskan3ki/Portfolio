"""Throttles pour le module User."""

from rest_framework.throttling import SimpleRateThrottle


class LoginThrottle(SimpleRateThrottle):
    """Limite les tentatives de connexion par IP."""

    scope = "login"

    def get_cache_key(self, request, _view):
        return self.get_ident(request)


class ResetPasswordThrottle(SimpleRateThrottle):
    """Limite les demandes de reinitialisation par IP."""

    scope = "reset_password"

    def get_cache_key(self, request, _view):
        return self.get_ident(request)


class ChangePasswordThrottle(SimpleRateThrottle):
    """Limite les changements de mot de passe par utilisateur."""

    scope = "change_password"

    def get_cache_key(self, request, _view):
        if request.user.is_authenticated:
            return f"change_password_{request.user.pk}"
        return self.get_ident(request)


class SessionThrottle(SimpleRateThrottle):
    """Limite les operations sur les sessions."""

    scope = "sessions"

    def get_cache_key(self, request, _view):
        if request.user.is_authenticated:
            return f"sessions_{request.user.pk}"
        return self.get_ident(request)
