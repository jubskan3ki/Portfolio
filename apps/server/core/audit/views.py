"""Vues pour le module audit."""

from rest_framework.permissions import IsAdminUser

from utils.api.mixins import ReadOnlyAPIViewSet

from .filters import AuditLogFilter
from .models import AuditLog
from .serializers import AuditLogDetailSerializer, AuditLogListSerializer
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
