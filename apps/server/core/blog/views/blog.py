"""
Gestion des articles de blog via API.
"""

from rest_framework import filters, permissions, viewsets
from rest_framework.parsers import JSONParser, MultiPartParser

from ..models import BlogPost
from ..serializers.blog import BlogPostSerializer
from ..throttles import BlogPostThrottle


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    CRUD des articles de blog.
    - Lecture publique.
    - Création, modification, suppression réservées aux admins authentifiés.
    """

    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    parser_classes = [MultiPartParser, JSONParser]
    throttle_classes = [BlogPostThrottle]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "category", "tags"]
    ordering_fields = ["created_at", "updated_at", "title"]

    def get_permissions(self):
        """
        Permissions :
        - SAFE_METHODS (GET, HEAD, OPTIONS) : Accès public.
        - POST, PUT, DELETE : Authentification requise.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
