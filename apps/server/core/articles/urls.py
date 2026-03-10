"""
Configuration des URLs pour l'application Articles.
Structure propre et cohérente avec routeurs DRF.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.article import ArticleViewSet
from .views.category import CategoryViewSet
from .views.tag import TagViewSet

# Création du routeur principal
router = DefaultRouter()

# Enregistrement des viewsets
router.register(r"categories", CategoryViewSet, basename="article-category")
router.register(r"tags", TagViewSet, basename="article-tag")
router.register(r"", ArticleViewSet, basename="article")

# Configuration des URLs
urlpatterns = [
    # Inclusion des routes générées par le routeur
    path("", include(router.urls)),
]
