"""
Gestion des articles de blog via API.
"""

from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser

from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    Vue API pour gérer les articles de blog.
    Seul l'admin authentifié peut créer, mettre à jour et supprimer.
    """

    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    parser_classes = [JSONParser, MultiPartParser]
