"""Configuration des URLs pour le module experiences."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExperienceTypeViewSet, ExperienceViewSet, StatsView, TimelineView

router = DefaultRouter()
router.register(r"types", ExperienceTypeViewSet, basename="experience-type")
router.register(r"", ExperienceViewSet, basename="experience")

urlpatterns = [
    path("stats/", StatsView.as_view(), name="experience-stats"),
    path("timeline/", TimelineView.as_view(), name="experience-timeline"),
    path("", include(router.urls)),
]
