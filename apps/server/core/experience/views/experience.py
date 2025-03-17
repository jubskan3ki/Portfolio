"""
Gestion des expériences via API.
"""

from rest_framework import filters, permissions, viewsets
from rest_framework.parsers import JSONParser, MultiPartParser

from ..models import Experience
from ..serializers.experience import ExperienceSerializer
from ..throttles import ExperienceThrottle


class ExperienceViewSet(viewsets.ModelViewSet):
    """
    CRUD des expériences professionnelles et éducatives.
    - Lecture publique.
    - Création/modification/suppression réservées aux utilisateurs authentifiés.
    """

    queryset = Experience.objects.all().order_by("-start_date")
    serializer_class = ExperienceSerializer
    parser_classes = [MultiPartParser, JSONParser]
    throttle_classes = [ExperienceThrottle]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "company_or_school", "experience_type"]
    ordering_fields = ["start_date", "end_date", "created_at"]

    def get_permissions(self):
        """
        SAFE_METHODS => accès public, sinon authentification requise.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
