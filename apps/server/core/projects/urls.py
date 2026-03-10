"""Configuration des URLs pour le module projects."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProjectViewSet, StatsView, StatusViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"statuses", StatusViewSet, basename="status")
router.register(r"", ProjectViewSet, basename="project")

urlpatterns = [
    path("stats/", StatsView.as_view(), name="project-stats"),
    path("", include(router.urls)),
]
