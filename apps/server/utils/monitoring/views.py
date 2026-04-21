"""Views pour exposer les metriques Prometheus."""

from django.http import HttpRequest, HttpResponse
from django.views import View
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest


class MetricsView(View):
    """GET /metrics/ | format Prometheus."""

    def get(self, _request: HttpRequest) -> HttpResponse:
        metrics = generate_latest()
        return HttpResponse(
            metrics,
            content_type=CONTENT_TYPE_LATEST,
        )
