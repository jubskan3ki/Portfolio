"""Vues pour les statistiques des projets."""

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, views
from rest_framework.request import Request
from rest_framework.response import Response

from ..doc import RESPONSE_200_STATS, TAGS_STATS
from ..services.stats import StatsService
from ..throttles import ProjectsThrottle


class StatsView(views.APIView):
    """API endpoint pour les statistiques des projets."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [ProjectsThrottle]

    @swagger_auto_schema(
        operation_summary="Statistiques des projets",
        operation_description="Recupere les statistiques globales des projets.",
        responses={200: RESPONSE_200_STATS},
        tags=TAGS_STATS,
    )
    def get(self, _request: Request) -> Response:
        """Recupere les statistiques des projets."""
        stats = StatsService.get_stats()
        return Response(stats)
