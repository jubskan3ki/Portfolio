"""
Routes API pour la gestion des articles de blog.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.blog import BlogPostViewSet

router = DefaultRouter()
router.register(r"", BlogPostViewSet, basename="blogposts")

urlpatterns = [
    path("", include(router.urls)),
]
