"""
Gestion des projets du portfolio via API.
"""

from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Vue API pour gérer les projets du portfolio.
    Seul l'admin authentifié peut créer, mettre à jour et supprimer.
    """

    queryset = Project.objects.all().order_by("-created_at")
    serializer_class = ProjectSerializer
    parser_classes = [JSONParser, MultiPartParser]
