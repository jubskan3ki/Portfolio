"""
Gestion des projets du portfolio via API.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from ..models import Project
from ..serializers.project import ProjectSerializer
from ..throttles import ProjectThrottle


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Vue enrichie pour gérer entièrement les projets :
    - Accès en lecture public.
    - Modifications restreintes aux utilisateurs authentifiés.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes = [MultiPartParser, JSONParser]
    throttle_classes = [ProjectThrottle]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["title", "tags", "description"]
    ordering_fields = ["created_at", "updated_at", "title", "priority", "start_date", "end_date"]
    filterset_fields = ["status", "priority"]

    def get_permissions(self):
        """
        SAFE_METHODS => accès public.
        Méthodes d'écriture => authentification obligatoire.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def active(self, request):
        """
        Retourne uniquement les projets actifs (planification ou en cours).
        """
        _ = request
        queryset = self.queryset.filter(status__in=["planning", "in_progress"])
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def recent(self, request):
        """
        Renvoie les 5 derniers projets créés.
        """
        _ = request
        recent_projects = self.queryset.order_by("-created_at")[:5]
        serializer = self.get_serializer(recent_projects, many=True)
        return Response(serializer.data)

    def archived(self, request):
        """
        Renvoie les projets archivés.
        """
        _ = request
        archived_projects = self.queryset.filter(status="archived")
        page = self.paginate_queryset(archived_projects)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(archived_projects, many=True)
        return Response(serializer.data)

    def by_tag(self, request):
        """
        Filtre les projets par un tag spécifique passé en paramètre.
        """
        tag = request.query_params.get("tag", None)
        if tag:
            projects_by_tag = self.queryset.filter(tags__icontains=tag)
            page = self.paginate_queryset(projects_by_tag)
            if page:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(projects_by_tag, many=True)
            return Response(serializer.data)
        return Response({"detail": "Veuillez spécifier un tag via le paramètre 'tag'."}, status=400)
