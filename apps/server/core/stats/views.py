"""Views pour le module Stats (Dashboard)."""

import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.exceptions.service import ValidationError as ServiceValidationError

from .serializers import (
    ChartDataSerializer,
    DashboardStatsSerializer,
    QuickStatsSerializer,
    RecentActivitySerializer,
    WebVitalsIngestSerializer,
    WebVitalsSummarySerializer,
)
from .services import StatsService, WebVitalsService
from .throttles import StatsThrottle, WebVitalsThrottle

logger = logging.getLogger("core.stats")


class DashboardStatsView(APIView):
    """Vue pour les statistiques du dashboard."""

    permission_classes = [IsAdminUser]
    throttle_classes = [StatsThrottle]

    @extend_schema(
        description="Recupere les statistiques globales du dashboard",
        responses={200: DashboardStatsSerializer},
    )
    def get(self, _request: Request) -> Response:
        """Retourne les statistiques du dashboard."""
        stats = StatsService.get_module_stats()
        return Response(stats, status=status.HTTP_200_OK)


class DashboardChartDataView(APIView):
    """Vue pour les donnees des graphiques."""

    permission_classes = [IsAdminUser]
    throttle_classes = [StatsThrottle]

    @extend_schema(
        description="Recupere les donnees pour les graphiques",
        responses={200: ChartDataSerializer},
    )
    def get(self, _request: Request) -> Response:
        """Retourne les donnees pour les graphiques."""
        chart_data = StatsService.get_chart_data()
        return Response(chart_data, status=status.HTTP_200_OK)


class DashboardActivityView(APIView):
    """Vue pour l'activite recente."""

    permission_classes = [IsAdminUser]
    throttle_classes = [StatsThrottle]

    @extend_schema(
        description="Recupere l'activite recente",
        responses={200: RecentActivitySerializer},
    )
    def get(self, request: Request) -> Response:
        """Retourne l'activite recente."""
        try:
            limit = min(int(request.query_params.get("limit", 10)), 50)
        except (ValueError, TypeError) as exc:
            raise ServiceValidationError("Le parametre 'limit' doit etre un entier.") from exc

        activities = StatsService.get_recent_activity(limit)
        return Response(
            {"activities": activities},
            status=status.HTTP_200_OK,
        )


class DashboardQuickStatsView(APIView):
    """Vue pour les stats rapides."""

    permission_classes = [IsAdminUser]
    throttle_classes = [StatsThrottle]

    @extend_schema(
        description="Recupere les stats rapides",
        responses={200: QuickStatsSerializer},
    )
    def get(self, _request: Request) -> Response:
        """Retourne les stats rapides."""
        quick_stats = StatsService.get_quick_stats()
        return Response(quick_stats, status=status.HTTP_200_OK)


class DashboardOverviewView(APIView):
    """Vue complete du dashboard avec toutes les donnees."""

    permission_classes = [IsAdminUser]
    throttle_classes = [StatsThrottle]

    @extend_schema(
        description="Recupere toutes les donnees du dashboard en une requete",
        responses={200: OpenApiResponse(description="Dashboard overview data")},
    )
    def get(self, _request: Request) -> Response:
        """Retourne toutes les donnees du dashboard."""
        return Response(
            StatsService.get_full_dashboard(),
            status=status.HTTP_200_OK,
        )


class WebVitalsIngestView(APIView):
    """Endpoint public d'ingestion des Web Vitals."""

    permission_classes = [AllowAny]
    throttle_classes = [WebVitalsThrottle]

    @extend_schema(
        description="Ingestion des metriques Web Vitals",
        request=WebVitalsIngestSerializer,
        responses={202: OpenApiResponse(description="Accepted")},
    )
    def post(self, request: Request) -> Response:
        """Accepte et persiste un evenement Web Vitals."""
        content_length = request.META.get("CONTENT_LENGTH")
        if content_length:
            try:
                if int(content_length) > 10_000:
                    raise ServiceValidationError("Payload trop volumineux.")
            except ValueError as exc:
                raise ServiceValidationError("En-tete Content-Length invalide.") from exc

        serializer = WebVitalsIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        WebVitalsService.ingest(data)

        logger.info(
            "web_vital name=%s value=%.2f rating=%s page=%s",
            data.get("name"),
            float(data.get("value", 0)),
            data.get("rating"),
            data.get("page"),
        )

        return Response({"status": "accepted"}, status=status.HTTP_202_ACCEPTED)


class WebVitalsSummaryView(APIView):
    """Endpoint admin de synthese des Web Vitals."""

    permission_classes = [IsAdminUser]
    throttle_classes = [StatsThrottle]

    @extend_schema(
        description="Synthese des Web Vitals sur une fenetre glissante",
        responses={200: WebVitalsSummarySerializer},
    )
    def get(self, request: Request) -> Response:
        """Retourne un resume agrege des metriques Web Vitals."""
        days_param = request.query_params.get("days", "7")
        try:
            days = max(1, min(int(days_param), 90))
        except (ValueError, TypeError) as exc:
            raise ServiceValidationError("Le parametre 'days' doit etre un entier.") from exc

        payload = WebVitalsService.summary(days)
        return Response(payload, status=status.HTTP_200_OK)
