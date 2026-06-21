"""Vues pour l'authentification des administrateurs."""

import logging
import uuid
from typing import Any, cast

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import DatabaseError, IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from utils.exceptions import AuthenticationError
from utils.security import (
    SessionManager,
    clear_auth_cookies,
    generate_fingerprint,
    get_refresh_token_from_cookie,
    set_access_cookie,
    set_auth_cookies,
)

from ..docs import LOGIN_RESPONSES, LOGOUT_RESPONSES, REFRESH_RESPONSES
from ..serializers.admin import AdminLoginSerializer, AdminProfileSerializer
from ..services.admin import AdminService
from ..throttles import LoginThrottle

logger = logging.getLogger(__name__)
User = get_user_model()


class AdminLoginView(APIView):
    """Connexion des administrateurs."""

    permission_classes = [AllowAny]
    throttle_classes = [LoginThrottle]

    @extend_schema(
        summary="Connexion administrateur",
        description="Authentifie un administrateur et renvoie des tokens JWT via cookies HTTPOnly.",
        request=AdminLoginSerializer,
        responses=LOGIN_RESPONSES,
        tags=["Users"],
    )
    def post(self, request):
        """Traite une demande de connexion admin."""
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict[str, Any], serializer.validated_data)

        fingerprint = generate_fingerprint(request)
        session_id = uuid.uuid4().hex

        try:
            auth_result = AdminService.login_user(
                email=data["email"],
                password=data["password"],
                session_id=session_id,
            )
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({"detail": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)
        except (ValueError, TypeError):
            return Response({"detail": "Format de donnees invalide"}, status=status.HTTP_400_BAD_REQUEST)
        except (IntegrityError, DatabaseError):
            return Response(
                {"detail": "Erreur de base de donnees"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        else:
            refresh_token = RefreshToken(auth_result["refresh"])
            refresh_jti = str(refresh_token.get("jti", ""))

            session_manager = SessionManager(auth_result["user"].id)
            session_manager.add_session(
                session_id,
                {
                    "browser": fingerprint.browser,
                    "os": fingerprint.os,
                    "is_mobile": fingerprint.is_mobile,
                    "ip_address": fingerprint.ip_address,
                    "refresh_jti": refresh_jti,
                },
            )

            response = Response(
                {"user": AdminProfileSerializer(auth_result["user"]).data},
                status=status.HTTP_200_OK,
            )
            return set_auth_cookies(
                response,
                auth_result["access"],
                auth_result["refresh"],
                remember=data.get("remember_me", False),
            )


class AdminLogoutView(APIView):
    """Deconnexion des administrateurs."""

    permission_classes = [AllowAny]

    @extend_schema(
        summary="Deconnexion administrateur",
        description="Invalide le token de rafraichissement JWT et supprime les cookies.",
        responses=LOGOUT_RESPONSES,
        tags=["Users"],
    )
    def post(self, request):
        """Traite une demande de deconnexion admin."""
        refresh_token = get_refresh_token_from_cookie(request)
        user_id = None
        session_id = None

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                user_id = token.get("user_id")
                session_id = token.get("session_id")
                if hasattr(token, "blacklist"):
                    token.blacklist()
            except (TokenError, ValueError, TypeError):
                pass

        if user_id and session_id:
            session_manager = SessionManager(user_id)
            session_manager.remove_session(session_id)

        response = Response({"detail": "Deconnexion reussie."}, status=status.HTTP_200_OK)
        return clear_auth_cookies(response)


class AdminRefreshView(APIView):
    """Rafraichissement des tokens JWT."""

    permission_classes = [AllowAny]

    @extend_schema(
        summary="Rafraichissement du token",
        description="Genere un nouveau token d'acces via cookie HTTPOnly.",
        responses=REFRESH_RESPONSES,
        tags=["Users"],
    )
    def post(self, request):
        """Traite une demande de rafraichissement de token."""
        refresh_token_str = get_refresh_token_from_cookie(request)

        if not refresh_token_str:
            return Response(
                {"detail": "Token de rafraichissement manquant"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            result = AdminService.refresh_session(refresh_token_str)
        except AuthenticationError as exc:
            response = Response({"detail": str(exc.detail)}, status=status.HTTP_401_UNAUTHORIZED)
            return clear_auth_cookies(response)
        except (ValueError, TypeError):
            response = Response({"detail": "Format invalide"}, status=status.HTTP_400_BAD_REQUEST)
            return clear_auth_cookies(response)
        except (AttributeError, KeyError, ImportError):
            return Response(
                {"detail": "Erreur lors du rafraichissement"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        new_access_token = result["access"]
        new_refresh_token = result["refresh"]

        response = Response({"detail": "Token rafraichi"}, status=status.HTTP_200_OK)
        if new_refresh_token:
            return set_auth_cookies(response, new_access_token, new_refresh_token)
        return set_access_cookie(response, new_access_token)
