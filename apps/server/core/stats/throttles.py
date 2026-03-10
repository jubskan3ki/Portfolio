"""Throttling pour le module Stats."""

from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle


class StatsThrottle(UserRateThrottle):
    """Limite le nombre de requetes stats par utilisateur."""

    scope = "stats"
    rate = "60/minute"


class WebVitalsThrottle(SimpleRateThrottle):
    """Limite les envois de Web Vitals par utilisateur/IP."""

    scope = "web_vitals"

    def get_cache_key(self, request, view) -> str | None:
        del view
        user = getattr(request, "user", None)
        ident = f"user:{user.pk}" if user and user.is_authenticated else f"anon:{self.get_ident(request)}"
        return self.cache_format % {
            "scope": self.scope,
            "ident": ident,
        }
