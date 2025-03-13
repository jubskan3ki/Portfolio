"""
Gestion des technologies et stacks via API.
"""

from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser

from .models import Stack
from .serializers import StackSerializer


class StackViewSet(viewsets.ModelViewSet):
    """
    Vue API pour gérer les technologies et stacks.
    Seul l'admin authentifié peut créer, mettre à jour et supprimer.
    """

    queryset = Stack.objects.all().order_by("-created_at")
    serializer_class = StackSerializer
    parser_classes = [JSONParser, MultiPartParser]
