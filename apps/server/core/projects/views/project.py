"""
Gestion des projets du portfolio via API.
"""

from rest_framework import filters, permissions, viewsets
from rest_framework.parsers import JSONParser, MultiPartParser

from ..models import Project
from ..serializers.project import ProjectSerializer
from ..throttles import ProjectThrottle


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Vue CRUD pour les projets :
    - Lecture : publique.
    - Écriture/modification/suppression : restreinte aux utilisateurs authentifiés.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes = [MultiPartParser, JSONParser]
    throttle_classes = [ProjectThrottle]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "tags"]
    ordering_fields = ["created_at", "updated_at", "title"]

    def get_permissions(self):
        """
        SAFE_METHODS => accès public.
        Méthodes d'écriture => authentification obligatoire.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
