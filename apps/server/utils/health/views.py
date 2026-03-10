"""Views pour les health checks."""

from typing import Any

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .checks import HealthStatus, run_all_checks


class HealthCheckView(APIView):
    """Endpoint de health check complet.

    GET /health/ - Retourne le status de sante de tous les services.

    Reponses:
        200: Tous les services sont healthy
        503: Au moins un service est unhealthy
    """

    permission_classes: list[Any] = [AllowAny]
    authentication_classes: list[Any] = []  # Pas d'auth requise
    throttle_classes: list[Any] = []  # Pas de throttling

    def get(self, _request: Request) -> Response:
        """Execute les health checks et retourne le resultat."""
        result = run_all_checks()

        # 503 si unhealthy, 200 sinon
        http_status = (
            status.HTTP_503_SERVICE_UNAVAILABLE
            if result["status"] == HealthStatus.UNHEALTHY.value
            else status.HTTP_200_OK
        )

        return Response(result, status=http_status)


class LivenessView(APIView):
    """Endpoint de liveness check (k8s).

    GET /health/live/ - Verifie que l'app repond.
    """

    permission_classes: list[Any] = [AllowAny]
    authentication_classes: list[Any] = []
    throttle_classes: list[Any] = []

    def get(self, _request: Request) -> Response:
        """Simple check que l'app est en vie."""
        return Response({"status": "alive"}, status=status.HTTP_200_OK)


class ReadinessView(APIView):
    """Endpoint de readiness check (k8s).

    GET /health/ready/ - Verifie que l'app est prete a recevoir du trafic.
    """

    permission_classes: list[Any] = [AllowAny]
    authentication_classes: list[Any] = []
    throttle_classes: list[Any] = []

    def get(self, _request: Request) -> Response:
        """Check que les dependances sont prets."""
        result = run_all_checks()

        if result["status"] == HealthStatus.UNHEALTHY.value:
            return Response(
                {"status": "not_ready", "checks": result["checks"]},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({"status": "ready"}, status=status.HTTP_200_OK)
