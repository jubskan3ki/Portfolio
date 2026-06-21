"""Vues pour la gestion des mots de passe."""

import logging
from typing import Any, cast

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..docs import CHANGE_PASSWORD_RESPONSES, REQUEST_RESET_RESPONSES, RESET_PASSWORD_RESPONSES
from ..serializers.password import ChangePasswordSerializer, RequestResetPasswordSerializer, ResetPasswordSerializer
from ..services.password import PasswordService
from ..throttles import ChangePasswordThrottle, ResetPasswordThrottle

logger = logging.getLogger("core.user")


class RequestResetPasswordView(APIView):
    """Demande de reinitialisation de mot de passe."""

    permission_classes = [AllowAny]
    throttle_classes = [ResetPasswordThrottle]

    @extend_schema(
        summary="Demander la reinitialisation",
        description="Envoie un email avec un code de reinitialisation.",
        request=RequestResetPasswordSerializer,
        responses=REQUEST_RESET_RESPONSES,
        tags=["Password"],
    )
    def post(self, request):
        """Traite une demande de reinitialisation de mot de passe."""
        try:
            serializer = RequestResetPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = cast(dict[str, Any], serializer.validated_data)
            PasswordService.request_password_reset(data["email"])
        except (ValidationError, serializers.ValidationError):
            logger.exception("Erreur de validation reinitialisation")

        # Toujours retourner succes pour securite (pas d'enumeration d'emails)
        return Response(
            {"detail": "Si votre email est valide, vous recevrez un code de reinitialisation."},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    """Reinitialisation du mot de passe."""

    permission_classes = [AllowAny]
    throttle_classes = [ResetPasswordThrottle]

    @extend_schema(
        summary="Reinitialiser le mot de passe",
        description="Reinitialise le mot de passe avec le code fourni.",
        request=ResetPasswordSerializer,
        responses=RESET_PASSWORD_RESPONSES,
        tags=["Password"],
    )
    def post(self, request):
        """Traite la reinitialisation effective du mot de passe."""
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict[str, Any], serializer.validated_data)

        try:
            PasswordService.reset_password(
                email=data["email"],
                reset_code=data["reset_code"],
                new_password=data["new_password"],
            )
        except ObjectDoesNotExist as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({"detail": "Format de donnees invalide"}, status=status.HTTP_400_BAD_REQUEST)
        except OSError:
            logger.exception("Erreur IO reinitialisation")
            return Response(
                {"detail": "Erreur systeme."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except (AttributeError, TypeError, ImportError):
            logger.exception("Erreur inattendue reinitialisation")
            return Response(
                {"detail": "Erreur interne du serveur."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        else:
            return Response(
                {"detail": "Votre mot de passe a ete reinitialise avec succes."},
                status=status.HTTP_200_OK,
            )


class ChangePasswordView(APIView):
    """Changement de mot de passe pour utilisateur connecte."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [ChangePasswordThrottle]

    @extend_schema(
        summary="Changer le mot de passe",
        description="Change le mot de passe de l'utilisateur connecte.",
        request=ChangePasswordSerializer,
        responses=CHANGE_PASSWORD_RESPONSES,
        tags=["Password"],
    )
    def post(self, request):
        """Traite le changement de mot de passe."""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict[str, Any], serializer.validated_data)

        # session_id du JWT courant : conserve l'appareil courant connecte,
        # les autres sessions/tokens sont revoques.
        auth = getattr(request, "auth", None)
        current_session_id = str(auth.get("session_id")) if auth and auth.get("session_id") else None

        try:
            PasswordService.change_password(
                user=request.user,
                old_password=data["old_password"],
                new_password=data["new_password"],
                except_session_id=current_session_id,
            )
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except (ValueError, TypeError):
            return Response({"detail": "Format de donnees invalide"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "Mot de passe modifie avec succes."},
                status=status.HTTP_200_OK,
            )
