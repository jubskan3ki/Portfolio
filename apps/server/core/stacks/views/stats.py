"""Views pour les statistiques des stacks."""

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, views
from rest_framework.request import Request
from rest_framework.response import Response

from ..doc import RESPONSE_200_STATS, TAGS_STATS
from ..services import StatsService
from ..throttles import StacksThrottle


class StatsView(views.APIView):
    """API endpoint pour les statistiques des stacks."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    throttle_classes = (StacksThrottle,)

    @extend_schema(
        summary="Statistiques des stacks",
        description="Recupere les statistiques globales des stacks techniques.",
        responses={200: RESPONSE_200_STATS},
        tags=TAGS_STATS,
    )
    def get(self, _request: Request) -> Response:
        """Recupere les statistiques des stacks."""
        stats = StatsService.get_stats()
        return Response(stats)
