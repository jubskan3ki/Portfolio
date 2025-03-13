"""
Gestion de l'administrateur unique via l'API.
"""

from django.contrib.auth import authenticate

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    AdminSerializer,
    RequestResetPasswordSerializer,
    ResetPasswordSerializer,
    UpdateAdminSerializer,
)
from .tasks import send_reset_password_email


class AdminLoginView(APIView):
    """
    Authentification de l'administrateur avec JWT.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        print(f"🛠 Tentative de login pour : {email}")

        if not email or not password:
            return Response({"error": "Email et mot de passe requis."}, status=status.HTTP_400_BAD_REQUEST)

        admin = authenticate(request=request, username=email, password=password)

        if not admin:
            print(f"❌ Échec de l'auth pour : {email}")
            return Response({"error": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(admin)

        print(f"✅ Login réussi pour : {email}")
        return Response({"access": str(refresh.access_token), "refresh": str(refresh)}, status=status.HTTP_200_OK)


class AdminView(APIView):
    """
    Gestion de l'administrateur unique : consultation et mise à jour.
    """

    def get(self, request):
        admin = request.user
        serializer = AdminSerializer(admin)
        return Response(serializer.data)

    def patch(self, request):
        admin = request.user
        serializer = UpdateAdminSerializer(admin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Mise à jour réussie"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestResetPasswordView(APIView):
    """
    Vue API pour demander un code de réinitialisation du mot de passe.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
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
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Mot de passe mis à jour."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
