"""Vues pour les statistiques de contact."""

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, views
from rest_framework.request import Request
from rest_framework.response import Response

from ..doc import RESPONSE_200_STATS, TAGS_STATS
from ..services import ContactStatsService
from ..throttles import ContactsThrottle


class ContactStatsView(views.APIView):
    """API endpoint pour les statistiques de contact."""

    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [ContactsThrottle]

    @swagger_auto_schema(
        operation_summary="Statistiques de contact",
        operation_description="Recupere les statistiques globales de contact.",
        responses={200: RESPONSE_200_STATS},
        tags=TAGS_STATS,
    )
    def get(self, _request: Request) -> Response:
        """Recupere les statistiques de contact."""
        stats = ContactStatsService.get_stats()
        return Response(stats)
