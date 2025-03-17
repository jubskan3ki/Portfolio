"""
Routes API pour la gestion des technologies et stacks.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.stack import StackViewSet

router = DefaultRouter()
router.register(r"", StackViewSet, basename="stacks")

urlpatterns = [
    path("", include(router.urls)),
]
