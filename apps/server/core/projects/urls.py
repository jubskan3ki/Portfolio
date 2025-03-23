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
    path("active/", ProjectViewSet.as_view({"get": "active"}), name="projects-active"),
    path("recent/", ProjectViewSet.as_view({"get": "recent"}), name="projects-recent"),
    path("archived/", ProjectViewSet.as_view({"get": "archived"}), name="projects-archived"),
    path("by-tag/", ProjectViewSet.as_view({"get": "by_tag"}), name="projects-by-tag"),
]
