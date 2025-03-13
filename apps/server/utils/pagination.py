"""
Pagination personnalisée pour les API DRF.
"""

from collections import OrderedDict

from django.conf import settings

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomPagination(LimitOffsetPagination):
    """
    Pagination personnalisée avec `limit` et `offset` pour les API DRF.
    Permet un contrôle plus granulaire sur la pagination des résultats.
    """

    default_limit = getattr(settings, "PAGE_SIZE", 10)
    max_limit = 100

    def get_paginated_response(self, data):
        """
        Retourne une réponse paginée avec `count`, `next`, `previous` et les données.
        """
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )
