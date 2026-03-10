"""Vues pour l'authentification des administrateurs."""

import logging
from typing import Any, cast

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import DatabaseError, IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

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

    @swagger_auto_schema(
        operation_summary="Connexion administrateur",
        operation_description="Authentifie un administrateur et renvoie des tokens JWT via cookies HTTPOnly.",
        request_body=AdminLoginSerializer,
        responses=LOGIN_RESPONSES,
        tags=["Users"],
    )
    def post(self, request):
        """Traite une demande de connexion admin."""
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict[str, Any], serializer.validated_data)

        # Generate fingerprint first to include in JWT
        fingerprint = generate_fingerprint(request)

        try:
            auth_result = AdminService.login_user(
                email=data["email"],
                password=data["password"],
                fingerprint_hash=fingerprint.fingerprint_hash,
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
            # Create session in SessionManager with refresh token JTI for revocation
            refresh_token = RefreshToken(auth_result["refresh"])
            refresh_jti = str(refresh_token.get("jti", ""))

            session_manager = SessionManager(auth_result["user"].id)
            session_manager.add_session(
                fingerprint.fingerprint_hash,
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

    @swagger_auto_schema(
        operation_summary="Deconnexion administrateur",
        operation_description="Invalide le token de rafraichissement JWT et supprime les cookies.",
        responses=LOGOUT_RESPONSES,
        tags=["Users"],
    )
    def post(self, request):
        """Traite une demande de deconnexion admin."""
        refresh_token = get_refresh_token_from_cookie(request)
        user_id = None

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                user_id = token.get("user_id")
                if hasattr(token, "blacklist"):
                    token.blacklist()
            except (TokenError, ValueError, TypeError):
                pass

        # Remove session from SessionManager
        if user_id:
            fingerprint = generate_fingerprint(request)
            session_manager = SessionManager(user_id)
            session_manager.remove_session(fingerprint.fingerprint_hash)

        response = Response({"detail": "Deconnexion reussie."}, status=status.HTTP_200_OK)
        return clear_auth_cookies(response)


class AdminRefreshView(APIView):
    """Rafraichissement des tokens JWT."""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Rafraichissement du token",
        operation_description="Genere un nouveau token d'acces via cookie HTTPOnly.",
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
            refresh_token = RefreshToken(refresh_token_str)

            # Validate fingerprint matches the one in refresh token
            token_fingerprint = refresh_token.get("fingerprint")
            if token_fingerprint:
                current_fingerprint = generate_fingerprint(request)
                if current_fingerprint.fingerprint_hash != token_fingerprint:
                    logger.warning(
                        "Fingerprint mismatch during refresh: expected %s, got %s",
                        token_fingerprint[:8],
                        current_fingerprint.fingerprint_hash[:8],
                    )
                    response = Response(
                        {"detail": "Session invalide"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                    return clear_auth_cookies(response)

            new_access_token = str(refresh_token.access_token)
            new_refresh_token = None

            simple_jwt_settings = getattr(settings, "SIMPLE_JWT", {})
            if simple_jwt_settings.get("ROTATE_REFRESH_TOKENS", False):
                if simple_jwt_settings.get("BLACKLIST_AFTER_ROTATION", False):
                    try:
                        refresh_token.blacklist()
                    except AttributeError:
                        logger.exception(
                            "Token blacklist method unavailable - "
                            "check rest_framework_simplejwt.token_blacklist is in INSTALLED_APPS"
                        )
                    except TokenError:
                        logger.exception("Failed to blacklist rotated refresh token")
                user_id = refresh_token.get("user_id")
                user = User.objects.get(id=user_id)
                new_refresh = RefreshToken.for_user(user)

                # Preserve fingerprint in new refresh token
                if token_fingerprint:
                    new_refresh["fingerprint"] = token_fingerprint
                    new_refresh.access_token["fingerprint"] = token_fingerprint

                new_refresh_token = str(new_refresh)

        except User.DoesNotExist:
            response = Response({"detail": "Utilisateur introuvable"}, status=status.HTTP_401_UNAUTHORIZED)
            return clear_auth_cookies(response)
        except TokenError:
            response = Response({"detail": "Token invalide ou expire"}, status=status.HTTP_401_UNAUTHORIZED)
            return clear_auth_cookies(response)
        except (ValueError, TypeError):
            response = Response({"detail": "Format invalide"}, status=status.HTTP_400_BAD_REQUEST)
            return clear_auth_cookies(response)
        except (AttributeError, KeyError, ImportError):
            return Response(
                {"detail": "Erreur lors du rafraichissement"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        response = Response({"detail": "Token rafraichi"}, status=status.HTTP_200_OK)
        if new_refresh_token:
            return set_auth_cookies(response, new_access_token, new_refresh_token)
        return set_access_cookie(response, new_access_token)
