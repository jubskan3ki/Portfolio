"""
Gestion des expériences via API.
"""

from rest_framework import filters, permissions, viewsets
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from ..models import Experience
from ..serializers.experience import ExperienceSerializer
from ..throttles import ExperienceThrottle


class ExperienceViewSet(viewsets.ModelViewSet):
    """
    CRUD complet avec vues personnalisées :
    - Lecture publique.
    - Écriture restreinte aux utilisateurs authentifiés.
    """

    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    parser_classes = [MultiPartParser, JSONParser]
    throttle_classes = [ExperienceThrottle]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "company_or_school", "experience_type", "location", "description"]
    ordering_fields = ["start_date", "end_date", "created_at", "updated_at"]

    def get_permissions(self):
        """
        SAFE_METHODS => accès public, sinon authentification requise.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def current(self, request):
        """
        Renvoie les expériences actuellement en cours.
        """
        _ = request
        current_exp = Experience.objects.current()
        page = self.paginate_queryset(current_exp)
        serializer = self.get_serializer(page, many=True) if page else self.get_serializer(current_exp, many=True)
        return self.get_paginated_response(serializer.data) if page else Response(serializer.data)

    def professional(self, request):
        """
        Renvoie uniquement les expériences professionnelles.
        """
        _ = request
        professional_exp = Experience.objects.professional()
        page = self.paginate_queryset(professional_exp)
        serializer = self.get_serializer(page, many=True) if page else self.get_serializer(professional_exp, many=True)
        return self.get_paginated_response(serializer.data) if page else Response(serializer.data)

    def educational(self, request):
        """
        Renvoie uniquement les expériences éducatives.
        """
        _ = request
        educational_exp = Experience.objects.educational()
        page = self.paginate_queryset(educational_exp)
        serializer = self.get_serializer(page, many=True) if page else self.get_serializer(educational_exp, many=True)
        return self.get_paginated_response(serializer.data) if page else Response(serializer.data)

    def highlighted(self, request):
        """
        Renvoie les expériences mises en avant dans le portfolio.
        """
        _ = request
        highlighted_exp = self.queryset.filter(is_highlighted=True)
        page = self.paginate_queryset(highlighted_exp)
        serializer = self.get_serializer(page, many=True) if page else self.get_serializer(highlighted_exp, many=True)
        return self.get_paginated_response(serializer.data) if page else Response(serializer.data)
