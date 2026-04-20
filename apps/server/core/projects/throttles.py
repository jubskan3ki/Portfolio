"""Throttles pour le module projects."""

from rest_framework.request import Request
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from utils.throttles.base import BaseModuleThrottle


class ProjectViewThrottle(AnonRateThrottle):
    """Throttle specifique pour le compteur de vues des projets."""

    scope = "project_view"


class ProjectsThrottle(BaseModuleThrottle):
    """
    Throttle pour les requetes sur les projets.

    Rates:
        - GET/HEAD/OPTIONS: 100/minute (lecture)
        - POST/PUT/PATCH/DELETE: 10/minute (ecriture)
    """

    scope = "projects"
    read_rate = "100/minute"
    write_rate = "10/minute"

    def get_cache_key(self, request: Request, view: APIView) -> str:
        """Genere une cle de cache unique pour le rate limiting."""
        ident = self.get_ident(request)
        method = request.method
        rate_type = "read" if method in {"GET", "HEAD", "OPTIONS"} else "write"
        view_name = view.__class__.__name__
        action = getattr(view, "action", None)

        if action == "view":
            return f"throttle_{self.scope}_{rate_type}_{view_name}_{action}_{ident}"

        return f"throttle_{self.scope}_{rate_type}_{view_name}_{method}_{ident}"
