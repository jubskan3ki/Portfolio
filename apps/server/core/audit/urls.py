"""URLs pour le module audit."""

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AuditLogViewSet, AuditStatsView

router = DefaultRouter()
router.register(r"logs", AuditLogViewSet, basename="audit-log")

urlpatterns = [
    path("stats/", AuditStatsView.as_view(), name="audit-stats"),
    *router.urls,
]
