"""Views pour les statistiques des stacks."""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, views
from rest_framework.request import Request
from rest_framework.response import Response

from ..doc import SCHEMA_STATS, TAGS_STATS
from ..services import StatsService
from ..throttles import StacksThrottle


class StatsView(views.APIView):
    """API endpoint pour les statistiques des stacks."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    throttle_classes = (StacksThrottle,)

    @swagger_auto_schema(
        operation_summary="Statistiques des stacks",
        operation_description="Recupere les statistiques globales des stacks techniques.",
        responses={200: openapi.Response(description="Statistiques", schema=SCHEMA_STATS)},
        tags=TAGS_STATS,
    )
    def get(self, _request: Request) -> Response:
        """Recupere les statistiques des stacks."""
        stats = StatsService.get_stats()
        return Response(stats)
