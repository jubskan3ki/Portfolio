"""
Vue CRUD pour la gestion des stacks.
"""

from rest_framework import filters, permissions, viewsets
from rest_framework.parsers import JSONParser, MultiPartParser

from ..models import Stack
from ..serializers.stack import StackSerializer
from ..throttles import StacksThrottle


class StackViewSet(viewsets.ModelViewSet):
    """
    Vue CRUD pour la gestion des stacks.
    - Lecture publique.
    - Écriture/modification/suppression restreinte aux utilisateurs authentifiés.
    """

    queryset = Stack.objects.all()
    serializer_class = StackSerializer
    parser_classes = [MultiPartParser, JSONParser]
    throttle_classes = [StacksThrottle]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category"]
    ordering_fields = ["created_at", "updated_at", "name"]

    def get_permissions(self):
        """
        Définition dynamique des permissions :
        - SAFE_METHODS (GET, HEAD, OPTIONS) => Public.
        - Autres => Authentification requise.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
