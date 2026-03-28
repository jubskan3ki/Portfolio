"""Vues pour la gestion du profil administrateur."""

from typing import Any, cast

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import DatabaseError, IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..docs import PROFILE_GET_RESPONSES, PROFILE_PUT_RESPONSES
from ..serializers.admin import AdminProfileSerializer, AdminUpdateProfileSerializer
from ..services.admin import AdminService


class AdminProfileView(APIView):
    """Gestion du profil administrateur."""

    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Obtenir le profil",
        description="Recupere le profil administrateur connecte.",
        responses=PROFILE_GET_RESPONSES,
        tags=["Users"],
    )
    def get(self, request):
        """Recupere le profil de l'administrateur connecte."""
        try:
            admin = AdminService.get_admin_profile(request.user.id)
        except ObjectDoesNotExist as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(AdminProfileSerializer(admin).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Mettre a jour le profil",
        description="Met a jour le profil administrateur connecte.",
        request=AdminUpdateProfileSerializer,
        responses=PROFILE_PUT_RESPONSES,
        tags=["Users"],
    )
    def put(self, request):
        """Met a jour le profil de l'administrateur connecte."""
        serializer = AdminUpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict[str, Any], serializer.validated_data)

        try:
            updated_admin = AdminService.update_admin_profile(
                user_id=request.user.id,
                profile_data=data,
            )
        except ObjectDoesNotExist as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except (IntegrityError, DatabaseError):
            return Response(
                {"detail": "Erreur de base de donnees"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except (ValueError, TypeError) as e:
            return Response({"detail": f"Format invalide: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(AdminProfileSerializer(updated_admin).data, status=status.HTTP_200_OK)
