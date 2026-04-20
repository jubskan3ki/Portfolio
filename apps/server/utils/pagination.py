"""Pagination DRF. Nouvelles APIs : APIResponsePagination uniquement."""

from django.conf import settings
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE_SIZE = getattr(settings, "PAGE_SIZE", 10)
MAX_PAGE_SIZE = 100


class APIResponsePagination(PageNumberPagination):
    """Reponse: {data, pagination: {total, page, limit, totalPages, next, previous}}."""

    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = "limit"
    max_page_size = MAX_PAGE_SIZE

    def get_paginated_response(self, data: list[dict[str, object]]) -> Response:
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


class StandardResultsSetPagination(APIResponsePagination):
    """DEPRECATED — kept for legacy APIs."""

    page_size_query_param = "page_size"


class CursorBasedPagination(CursorPagination):
    """Curseur : infinite scroll / real-time feeds uniquement."""

    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = "page_size"
    max_page_size = MAX_PAGE_SIZE
    ordering = "-created_at"

    def get_paginated_response(self, data: list[dict[str, object]]) -> Response:
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


CustomPagination = APIResponsePagination
