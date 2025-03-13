"""
Gestion des messages de contact via API.
"""

from rest_framework import generics, status
from rest_framework.response import Response

from .models import ContactMessage
from .serializers import ContactMessageSerializer
from .tasks import send_contact_email


class ContactMessageCreateView(generics.CreateAPIView):
    """
    Vue API pour soumettre un message de contact.
    Accessible sans authentification.
    """

    queryset = ContactMessage.objects.all().order_by("-created_at")
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            contact_message = serializer.save()

            # Envoyer un email à l'admin après enregistrement du message
            send_contact_email.delay(
                contact_message.name,
                contact_message.email,
                contact_message.message,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
