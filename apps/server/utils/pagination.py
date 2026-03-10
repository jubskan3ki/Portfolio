"""Pagination personnalisee pour les API DRF.

IMPORTANT: Utiliser uniquement APIResponsePagination pour toutes les nouvelles APIs.
Les autres classes sont conservees pour compatibilite mais sont depreciees.
"""

from django.conf import settings
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE_SIZE = getattr(settings, "PAGE_SIZE", 10)
MAX_PAGE_SIZE = 100


class APIResponsePagination(PageNumberPagination):
    """Pagination unifiee pour toutes les API endpoints.

    C'est la classe de pagination RECOMMANDEE pour toutes les nouvelles APIs.

    Format de reponse:
    {
        "data": [...],
        "pagination": {
            "total": int,
            "page": int,
            "limit": int,
            "totalPages": int,
            "next": str | null,
            "previous": str | null
        }
    }
    """

    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = "limit"
    max_page_size = MAX_PAGE_SIZE

    def get_paginated_response(self, data: list[dict[str, object]]) -> Response:
        """Retourne la reponse paginee au format unifie."""
        page = self.page
        request = self.request
        if page is None or request is None:
            return Response({"data": data, "pagination": {}})
        return Response(
            {
                "data": data,
                "pagination": {
                    "total": page.paginator.count,
                    "page": page.number,
                    "limit": self.get_page_size(request),
                    "totalPages": page.paginator.num_pages,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
            }
        )


# =============================================================================
# CLASSES DEPRECIEES - Conservees pour compatibilite uniquement
# Utiliser APIResponsePagination pour les nouvelles APIs
# =============================================================================


class StandardResultsSetPagination(APIResponsePagination):
    """DEPRECATED: Utiliser APIResponsePagination a la place.

    Conservee pour compatibilite avec les anciennes APIs.
    """

    page_size_query_param = "page_size"


class CursorBasedPagination(CursorPagination):
    """Pagination par curseur, ideale pour les flux infinis.

    Utiliser uniquement pour les cas specifiques (infinite scroll, real-time feeds).
    Pour la plupart des cas, preferer APIResponsePagination.
    """

    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = "page_size"
    max_page_size = MAX_PAGE_SIZE
    ordering = "-created_at"

    def get_paginated_response(self, data: list[dict[str, object]]) -> Response:
        """Retourne une reponse paginee avec format standardise."""
        request = getattr(self, "request", None)
        limit = self.get_page_size(request) if request else self.page_size
        return Response(
            {
                "data": data,
                "pagination": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "limit": limit,
                },
            }
        )


# Alias pour compatibilite
CustomPagination = APIResponsePagination
