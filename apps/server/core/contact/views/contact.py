"""
Gestion des messages de contact via API.
"""

from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from ..models import ContactMessage
from ..serializers.contact import ContactMessageSerializer
from ..tasks import send_contact_email
from ..throttles import ContactMessageThrottle


class ContactMessageCreateView(generics.CreateAPIView):
    """
    Vue API pour soumettre un message de contact.
    Accessible sans authentification.
    """

    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    parser_classes = [JSONParser]
    throttle_classes = [ContactMessageThrottle]
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            contact_message = serializer.save()

            send_contact_email.delay(
                contact_message.name,
                contact_message.email,
                contact_message.message,
            )

            return Response(
                {"message": "Votre message a bien été envoyé. Nous vous contacterons bientôt."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
