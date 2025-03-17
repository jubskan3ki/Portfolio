"""
Routes API pour la gestion des projets.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.project import ProjectViewSet

router = DefaultRouter()
router.register(r"", ProjectViewSet, basename="projects")

urlpatterns = [
    path("", include(router.urls)),
]
