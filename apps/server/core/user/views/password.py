"""
Gestion de l'administrateur unique via l'API.
"""

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.password import (
    RequestResetPasswordSerializer,
    ResetPasswordSerializer,
)
from ..tasks import send_reset_password_email
from ..throttles import ResetPasswordThrottle


class RequestResetPasswordView(APIView):
    """
    Vue API pour demander un code de réinitialisation du mot de passe.
    """

    permission_classes = [permissions.AllowAny]
    throttle_classes = [ResetPasswordThrottle]

    def post(self, request):
        """
        Envoi du code de réinitialisation par email.
        """
        serializer = RequestResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            send_reset_password_email.delay(serializer.validated_data["email"])
            return Response({"message": "Un code de réinitialisation a été envoyé."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
    Vue API pour valider le code de réinitialisation et changer le mot de passe en une seule étape.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Validation du code et mise à jour du mot de passe.
        """
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Mot de passe mis à jour."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
