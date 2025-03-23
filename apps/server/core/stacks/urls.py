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
    path("category/<str:category>/", StackViewSet.as_view({"get": "by_category"}), name="stacks-by-category"),
    path("most-proficient/", StackViewSet.as_view({"get": "most_proficient"}), name="stacks-most-proficient"),
]
