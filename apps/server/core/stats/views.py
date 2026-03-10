"""Views pour le module Stats (Dashboard)."""

import logging
from collections import defaultdict
from datetime import timedelta
from statistics import fmean

from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.exceptions.service import ValidationError as ServiceValidationError

from .models import WebVitalEvent
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

    @swagger_auto_schema(
        operation_description="Recupere les statistiques globales du dashboard",
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

    @swagger_auto_schema(
        operation_description="Recupere les donnees pour les graphiques",
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

    @swagger_auto_schema(
        operation_description="Recupere l'activite recente",
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

    @swagger_auto_schema(
        operation_description="Recupere les stats rapides",
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

    @swagger_auto_schema(
        operation_description="Recupere toutes les donnees du dashboard en une requete",
        responses={200: "Dashboard overview data"},
    )
    def get(self, _request: Request) -> Response:
        """Retourne toutes les donnees du dashboard."""
        return Response(
            StatsService.get_full_dashboard(),
            status=status.HTTP_200_OK,
        )


def _percentile(values: list[float], percentile: int) -> float | None:
    """Calcule un percentile simple sur une liste triee."""
    if not values:
        return None

    sorted_values = sorted(values)
    index = round((len(sorted_values) - 1) * (percentile / 100))
    return float(sorted_values[index])


class WebVitalsIngestView(APIView):
    """Endpoint public d'ingestion des Web Vitals."""

    permission_classes = [AllowAny]
    throttle_classes = [WebVitalsThrottle]

    @swagger_auto_schema(
        operation_description="Ingestion des metriques Web Vitals",
        request_body=WebVitalsIngestSerializer,
        responses={202: "Accepted"},
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

        WebVitalsService.ingest(serializer.validated_data)

        return Response({"status": "accepted"}, status=status.HTTP_202_ACCEPTED)


class WebVitalsSummaryView(APIView):
    """Endpoint admin de synthese des Web Vitals."""

    permission_classes = [IsAdminUser]
    throttle_classes = [StatsThrottle]

    @swagger_auto_schema(
        operation_description="Synthese des Web Vitals sur une fenetre glissante",
        responses={200: WebVitalsSummarySerializer},
    )
    def get(self, request: Request) -> Response:
        """Retourne un resume agrege des metriques Web Vitals."""
        days_param = request.query_params.get("days", "7")
        try:
            days = max(1, min(int(days_param), 90))
        except (ValueError, TypeError) as exc:
            raise ServiceValidationError("Le parametre 'days' doit etre un entier.") from exc

        since = timezone.now() - timedelta(days=days)
        events = list(WebVitalEvent.objects.filter(created_at__gte=since).values("metric_name", "value", "rating"))

        grouped_values: dict[str, list[float]] = defaultdict(list)
        default_ratings = {"good": 0, "needs-improvement": 0, "poor": 0}

        def _make_default_ratings() -> dict[str, int]:
            return default_ratings.copy()

        grouped_ratings: dict[str, dict[str, int]] = defaultdict(_make_default_ratings)

        for event in events:
            metric_name = str(event["metric_name"])
            metric_value = float(event["value"])
            rating = str(event["rating"])
            grouped_values[metric_name].append(metric_value)
            if rating in grouped_ratings[metric_name]:
                grouped_ratings[metric_name][rating] += 1

        metrics_summary = []
        for metric_name in sorted(grouped_values.keys()):
            values = grouped_values[metric_name]
            metrics_summary.append(
                {
                    "metric_name": metric_name,
                    "count": len(values),
                    "mean": round(float(fmean(values)), 2) if values else None,
                    "p75": _percentile(values, 75),
                    "p95": _percentile(values, 95),
                    "ratings": grouped_ratings[metric_name],
                }
            )

        payload = {
            "window_days": days,
            "total_events": len(events),
            "metrics": metrics_summary,
        }
        return Response(payload, status=status.HTTP_200_OK)
