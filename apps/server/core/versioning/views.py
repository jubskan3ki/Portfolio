"""Endpoints versioning : liste versions, restore, trash management."""

from __future__ import annotations

from typing import Any

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import VersionSerializer
from .services import (
    ObjectNotFoundError,
    UnknownModelError,
    UnsupportedModelError,
    VersionNotFoundError,
    list_trashed,
    list_versions,
    restore_version,
    untrash,
)


@extend_schema(
    tags=["Versioning"],
    summary="Liste les versions d'un objet",
    parameters=[
        OpenApiParameter(name="model", type=OpenApiTypes.STR, required=True, location="query"),
        OpenApiParameter(name="object_id", type=OpenApiTypes.STR, required=True, location="query"),
    ],
    responses={200: VersionSerializer(many=True)},
)
class VersionListView(APIView):
    """GET /api/versioning/versions/?model=Article&object_id=5."""

    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        model_name = request.query_params.get("model")
        object_id = request.query_params.get("object_id")
        if not model_name or not object_id:
            return Response(
                {"detail": "model et object_id sont requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        versions = list_versions(model_name, object_id)
        return Response(VersionSerializer(versions, many=True).data)


@extend_schema(
    tags=["Versioning"],
    summary="Restaure un objet a une version donnee",
    request=None,
    responses={
        200: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    },
)
class VersionRestoreView(APIView):
    """POST /api/versioning/restore/<version_id>/."""

    permission_classes = [IsAdminUser]

    def post(self, request: Request, version_id: int) -> Response:
        del request
        try:
            instance = restore_version(int(version_id))
        except VersionNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except UnknownModelError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "restored": True,
                "model": instance.__class__.__name__,
                "id": instance.pk,
            }
        )


@extend_schema(
    tags=["Versioning"],
    summary="Liste les objets soft-deleted d'un modele",
    parameters=[
        OpenApiParameter(name="model", type=OpenApiTypes.STR, required=True, location="query"),
    ],
    responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
)
class TrashListView(APIView):
    """GET /api/versioning/trashed/?model=Article."""

    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        model_name = request.query_params.get("model")
        if not model_name:
            return Response({"detail": "model requis."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            trashed = list_trashed(model_name)
        except UnknownModelError:
            return Response({"detail": f"Modele inconnu : {model_name}"}, status=status.HTTP_400_BAD_REQUEST)
        except UnsupportedModelError:
            return Response(
                {"detail": f"Modele {model_name} ne supporte pas le soft-delete."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(trashed)


@extend_schema(
    tags=["Versioning"],
    summary="Restaure un objet soft-deleted",
    request=None,
    responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
)
class UntrashView(APIView):
    """POST /api/versioning/untrash/?model=Article&object_id=5."""

    permission_classes = [IsAdminUser]

    def post(self, request: Request) -> Response:
        model_name = request.query_params.get("model")
        object_id = request.query_params.get("object_id")
        if not model_name or not object_id:
            return Response(
                {"detail": "model et object_id sont requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            instance: Any = untrash(model_name, object_id)
        except (UnknownModelError, UnsupportedModelError):
            return Response(
                {"detail": f"Modele {model_name} invalide ou sans soft-delete."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ObjectNotFoundError:
            return Response({"detail": "Objet introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"restored": True, "id": instance.pk})
