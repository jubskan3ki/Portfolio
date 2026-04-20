"""Vues pour le module audit."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.api.mixins import ReadOnlyAPIViewSet

from .filters import AuditLogFilter
from .models import AuditLog
from .serializers import AuditLogDetailSerializer, AuditLogListSerializer
from .services import (
    DEFAULT_STATS_WINDOW_DAYS,
    DEFAULT_TOP_N,
    compute_stats,
    get_object_timeline,
)
from .throttles import AuditThrottle


class AuditLogViewSet(ReadOnlyAPIViewSet):
    """ViewSet en lecture seule pour consulter les logs d'audit."""

    permission_classes = [IsAdminUser]
    throttle_classes = [AuditThrottle]
    filterset_class = AuditLogFilter
    serializer_classes = {
        "list": AuditLogListSerializer,
        "detail": AuditLogDetailSerializer,
    }

    def get_queryset(self):
        """Retourne les logs d'audit (select_related gere par AuditLogManager)."""
        return AuditLog.objects.all()

    @extend_schema(
        tags=["Audit"],
        summary="Timeline d'un objet audite",
        description="Tous les logs pour un couple (model_name, object_id), plus recent d'abord.",
        parameters=[
            OpenApiParameter(name="model", type=OpenApiTypes.STR, required=True, location="query"),
            OpenApiParameter(name="id", type=OpenApiTypes.STR, required=True, location="query"),
        ],
        responses={200: AuditLogDetailSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="timeline")
    def timeline(self, request: Request) -> Response:
        """Historique d'un objet precis."""
        model_name = request.query_params.get("model")
        object_id = request.query_params.get("id")
        if not model_name or not object_id:
            return Response(
                {"detail": "Les parametres 'model' et 'id' sont requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        logs = get_object_timeline(model_name, object_id)
        serializer = AuditLogDetailSerializer(logs, many=True)
        return Response(serializer.data)


class AuditStatsView(APIView):
    """Agregations analytiques sur les audit logs."""

    permission_classes = [IsAdminUser]
    throttle_classes = [AuditThrottle]

    @extend_schema(
        tags=["Audit"],
        summary="Statistiques d'audit",
        description=(
            "Agrege les audit logs sur la fenetre glissante demandee : total, "
            "repartition par action, top modeles, top utilisateurs, activite par jour."
        ),
        parameters=[
            OpenApiParameter(
                name="window_days",
                type=OpenApiTypes.INT,
                required=False,
                description=f"Fenetre en jours (defaut {DEFAULT_STATS_WINDOW_DAYS}).",
            ),
            OpenApiParameter(
                name="top_n",
                type=OpenApiTypes.INT,
                required=False,
                description=f"Taille des tops (defaut {DEFAULT_TOP_N}).",
            ),
        ],
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request: Request) -> Response:
        try:
            window_days = int(request.query_params.get("window_days", DEFAULT_STATS_WINDOW_DAYS))
            top_n = int(request.query_params.get("top_n", DEFAULT_TOP_N))
        except ValueError:
            return Response(
                {"detail": "Parametres invalides."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if window_days <= 0 or top_n <= 0:
            return Response(
                {"detail": "window_days et top_n doivent etre > 0."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(compute_stats(window_days=window_days, top_n=top_n))
