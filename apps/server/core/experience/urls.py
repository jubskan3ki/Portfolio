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
]
