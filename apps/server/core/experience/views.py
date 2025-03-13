"""
Gestion des expériences via API.
"""

from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser

from .models import Experience
from .serializers import ExperienceSerializer


class ExperienceViewSet(viewsets.ModelViewSet):
    """
    Vue API pour gérer les expériences (travail et éducation).
    Seul l'admin authentifié peut créer, mettre à jour et supprimer.
    """

    queryset = Experience.objects.all().order_by("-created_at")
    serializer_class = ExperienceSerializer
    parser_classes = [JSONParser, MultiPartParser]
