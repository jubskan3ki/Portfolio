"""
Gestion de l'administrateur unique via l'API.
"""

from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.admin import AdminSerializer, UpdateAdminSerializer
from ..throttles import LoginThrottle


class AdminLoginView(APIView):
    """
    Authentification de l'administrateur avec JWT.
    """

    permission_classes = [permissions.AllowAny]
    throttle_classes = [LoginThrottle]

    def post(self, request):
        """
        Authentification de l'administrateur avec JWT.
        """
        email = request.data.get("email")
        password = request.data.get("password")

        print(f"🛠 Tentative de login pour : {email}")

        if not email or not password:
            return Response(
                {"error": "Email et mot de passe requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        admin = authenticate(request=request, username=email, password=password)

        if not admin:
            return Response(
                {"error": "Identifiants invalides."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(admin)

        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status=status.HTTP_200_OK,
        )


class AdminLogoutView(APIView):
    """
    Déconnexion de l'administrateur.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Déconnexion de l'administrateur.
        """

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token manquant."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except (TokenError, InvalidToken):
            return Response(
                {"error": "Token invalide ou déjà blacklisté."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "Déconnexion réussie."}, status=status.HTTP_205_RESET_CONTENT)


class AdminProfileView(APIView):
    """
    Gestion de l'administrateur unique : consultation et mise à jour.
    """

    def get(self, request):
        """
        Consultation des informations de l'admin.
        """
        serializer = AdminSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """
        Mise à jour des informations de l'admin.
        """
        serializer = UpdateAdminSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Mise à jour réussie", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
