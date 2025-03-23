"""
Gestion des articles de blog via API.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import BlogPost
from ..serializers.blog import BlogPostSerializer
from ..throttles import BlogPostThrottle


class BlogPostViewSet(ModelViewSet):
    """
    Vue API complète pour les articles de blog :
    - Lecture publique.
    - Gestion réservée aux utilisateurs authentifiés.
    """

    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    parser_classes = [MultiPartParser, JSONParser]
    throttle_classes = [BlogPostThrottle]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["title", "category", "tags", "author"]
    ordering_fields = ["published_at", "created_at", "updated_at", "title", "views_count"]
    filterset_fields = ["status", "category", "author"]

    def get_permissions(self):
        """
        Gestion des permissions :
        - Méthodes sécurisées accessibles à tous.
        - Création, modification, suppression uniquement pour les utilisateurs authentifiés.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        """
        Augmente le compteur de vues à chaque affichage détaillé.
        """
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=["views_count"])
        return super().retrieve(request, *args, **kwargs)

    def recent(self, request):
        """
        Retourne les 5 articles récents publiés.
        """
        _ = request

        recent_posts = BlogPost.objects.published()[:5]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)

    def popular(self, request):
        """
        Retourne les articles les plus consultés (top 5).
        """
        _ = request
        popular_posts = BlogPost.objects.published().order_by("-views_count")[:5]
        serializer = self.get_serializer(popular_posts, many=True)
        return Response(serializer.data)

    def drafts(self, request):
        """
        Retourne les articles en brouillon, accès réservé aux utilisateurs authentifiés.
        """
        _ = request

        draft_posts = BlogPost.objects.drafts()
        page = self.paginate_queryset(draft_posts)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(draft_posts, many=True)
        return Response(serializer.data)
