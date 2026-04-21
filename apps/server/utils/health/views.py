"""Views pour les health checks."""

from typing import Any

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .checks import HealthStatus, run_all_checks


class HealthCheckView(APIView):
    """GET /health/ : 200 si tous healthy, 503 sinon."""

    permission_classes: list[Any] = [AllowAny]
    authentication_classes: list[Any] = []
    throttle_classes: list[Any] = []

    def get(self, _request: Request) -> Response:
        result = run_all_checks()

        http_status = (
            status.HTTP_503_SERVICE_UNAVAILABLE
            if result["status"] == HealthStatus.UNHEALTHY.value
            else status.HTTP_200_OK
        )

        return Response(result, status=http_status)


class LivenessView(APIView):
    """k8s liveness | app repond."""

    permission_classes: list[Any] = [AllowAny]
    authentication_classes: list[Any] = []
    throttle_classes: list[Any] = []

    def get(self, _request: Request) -> Response:
        return Response({"status": "alive"}, status=status.HTTP_200_OK)


class ReadinessView(APIView):
    """k8s readiness | dependances pretes."""

    permission_classes: list[Any] = [AllowAny]
    authentication_classes: list[Any] = []
    throttle_classes: list[Any] = []

    def get(self, _request: Request) -> Response:
        result = run_all_checks()

        if result["status"] == HealthStatus.UNHEALTHY.value:
            return Response(
                {"status": "not_ready", "checks": result["checks"]},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({"status": "ready"}, status=status.HTTP_200_OK)
