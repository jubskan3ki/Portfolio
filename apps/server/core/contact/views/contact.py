"""
Gestion des messages de contact via API.
"""

from rest_framework import filters, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import ContactMessage
from ..serializers.contact import ContactMessageSerializer
from ..tasks import send_contact_email
from ..throttles import ContactMessageThrottle


class ContactMessageViewSet(ModelViewSet):
    """
    Vue API complète pour gérer les messages de contact.
    - Création ouverte à tous.
    - Lecture, modification et suppression réservées aux administrateurs.
    """

    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    parser_classes = [JSONParser]
    throttle_classes = [ContactMessageThrottle]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "email", "subject", "message"]
    ordering_fields = ["created_at", "name", "subject"]
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        """
        Création (POST) accessible publiquement.
        Autres actions réservées aux administrateurs authentifiés.
        """
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        """
        Crée un nouveau message de contact et envoie les emails associés.
        """
        contact_message = serializer.save()
        # Envoi du mail via Celery
        send_contact_email.delay(
            contact_message.name,
            contact_message.email,
            contact_message.message,
        )

    def unread(self, request):
        """
        Retourne les messages non lus uniquement.
        """
        _ = request
        unread_messages = self.queryset.filter(is_read=False)
        serializer = self.get_serializer(unread_messages, many=True)
        return Response(serializer.data)

    def mark_as_read(self, request):
        """
        Marque un message spécifique comme lu.
        """
        _ = request
        contact_message = self.get_object()
        if not contact_message.is_read:
            contact_message.is_read = True
            contact_message.save(update_fields=["is_read"])
            return Response({"status": "Message marqué comme lu."})
        return Response({"status": "Le message était déjà marqué comme lu."})
