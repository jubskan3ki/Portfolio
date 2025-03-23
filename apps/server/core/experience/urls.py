"""
Routes API pour la gestion des expériences professionnelles et éducatives.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.experience import ExperienceViewSet

router = DefaultRouter()
router.register(r"", ExperienceViewSet, basename="experience")

urlpatterns = [
    path("", include(router.urls)),
    path("current/", ExperienceViewSet.as_view({"get": "current"}), name="experience-current"),
    path("professional/", ExperienceViewSet.as_view({"get": "professional"}), name="experience-professional"),
    path("educational/", ExperienceViewSet.as_view({"get": "educational"}), name="experience-educational"),
    path("highlighted/", ExperienceViewSet.as_view({"get": "highlighted"}), name="experience-highlighted"),
]
