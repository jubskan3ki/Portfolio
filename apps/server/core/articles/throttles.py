"""Throttling personnalise pour les articles."""

from rest_framework.request import Request
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from utils.throttles.base import BaseModuleThrottle


class ArticlesThrottle(BaseModuleThrottle):
    """
    Throttle pour limiter les actions sur les articles.

    Rates:
        - GET/HEAD/OPTIONS: 100/minute (lecture)
        - POST/PUT/PATCH/DELETE: 10/minute (ecriture)
    """

    scope = "articles"
    read_rate = "100/minute"
    write_rate = "10/minute"


class ArticleViewThrottle(UserRateThrottle):
    """Throttle specifique pour les vues d'articles (limite par utilisateur)."""

    scope = "article_view"

    def allow_request(self, request: Request, view: APIView) -> bool:
        """Autorise les utilisateurs authentifies."""
        if request.user and request.user.is_authenticated:
            return True
        return super().allow_request(request, view)
