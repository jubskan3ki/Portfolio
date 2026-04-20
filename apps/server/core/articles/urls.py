"""URLs pour l'application Articles."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.article import ArticleViewSet
from .views.category import CategoryViewSet
from .views.tag import TagViewSet

router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="article-category")
router.register(r"tags", TagViewSet, basename="article-tag")
router.register(r"", ArticleViewSet, basename="article")

urlpatterns = [
    path("", include(router.urls)),
]
