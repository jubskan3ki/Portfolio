"""Vues pour les statistiques des experiences."""

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, views
from rest_framework.request import Request
from rest_framework.response import Response

from ..doc import RESPONSE_200_STATS, RESPONSE_200_TIMELINE, TAGS_STATS
from ..serializers import ExperienceTimelineSerializer
from ..services import StatsService, TimelineService
from ..throttles import ExperienceThrottle


class StatsView(views.APIView):
    """API endpoint pour les statistiques des experiences."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    throttle_classes = (ExperienceThrottle,)

    @swagger_auto_schema(
        operation_summary="Statistiques des experiences",
        operation_description="Recupere les statistiques globales des experiences.",
        responses={200: RESPONSE_200_STATS},
        tags=TAGS_STATS,
    )
    def get(self, _request: Request) -> Response:
        """Recupere les statistiques des experiences."""
        stats = StatsService.get_stats()
        return Response(stats)


class TimelineView(views.APIView):
    """API endpoint pour la timeline des experiences."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    throttle_classes = (ExperienceThrottle,)

    @swagger_auto_schema(
        operation_summary="Timeline des experiences",
        operation_description="Recupere les experiences groupees par annee.",
        responses={200: RESPONSE_200_TIMELINE},
        tags=TAGS_STATS,
    )
    def get(self, _request: Request) -> Response:
        """Recupere la timeline des experiences."""
        timeline = TimelineService.get_timeline()
        serializer = ExperienceTimelineSerializer(timeline, many=True)
        return Response(serializer.data)
