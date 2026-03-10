"""URLs pour le module Stacks."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ResourceViewSet, StackViewSet, StatsView

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"resources", ResourceViewSet, basename="resource")
router.register(r"", StackViewSet, basename="stack")

urlpatterns = [
    path("stats/", StatsView.as_view(), name="stack-stats"),
    path("", include(router.urls)),
]
