"""
Vue CRUD pour la gestion des stacks.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from ..models import Stack
from ..serializers.stack import StackSerializer
from ..throttles import StacksThrottle


class StackViewSet(viewsets.ModelViewSet):
    """
    Vue CRUD enrichie pour la gestion complète des stacks :
    - Lecture publique avec recherche, filtrage et tri avancé.
    - Création/Modification/Suppression réservée aux utilisateurs authentifiés.
    """

    queryset = Stack.objects.all()
    serializer_class = StackSerializer
    parser_classes = [MultiPartParser, JSONParser]
    throttle_classes = [StacksThrottle]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "proficiency", "experience_years"]
    search_fields = ["name", "description", "category"]
    ordering_fields = ["created_at", "updated_at", "name", "proficiency", "experience_years"]
    ordering = ["-created_at"]

    def get_permissions(self):
        """
        Permissions dynamiques :
        - Lecture publique.
        - Écriture restreinte aux utilisateurs authentifiés.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Actions spécifiques lors de la création (audit/log, etc.).
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Actions spécifiques lors de la mise à jour.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Actions spécifiques lors de la suppression (archivage éventuel, logging).
        """
        instance.delete()

    def by_category(self, request, category=None):
        """
        Renvoie les stacks d'une catégorie spécifique.
        """
        _ = request
        queryset = self.queryset.filter(category=category)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def most_proficient(self, request):
        """
        Renvoie les stacks les plus maîtrisés, triés par compétence puis années d'expérience.
        """
        _ = request
        queryset = self.queryset.order_by("-proficiency", "-experience_years")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
