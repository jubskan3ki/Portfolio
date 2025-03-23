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
    path("recent/", BlogPostViewSet.as_view({"get": "recent"}), name="blogpost-recent"),
    path("popular/", BlogPostViewSet.as_view({"get": "popular"}), name="blogpost-popular"),
    path("drafts/", BlogPostViewSet.as_view({"get": "drafts"}), name="blogpost-drafts"),
]
