"""Vues pour les soumissions de contact."""

import logging
from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from config.permissions import AllowAnonymousCreate, IsAdminOnly
from utils.api import BaseAPIViewSet
from utils.network import get_client_ip

from ..doc import (
    RESPONSE_201_CONTACT,
    RESPONSE_204,
    RESPONSE_400,
    RESPONSE_401,
    RESPONSE_403,
    RESPONSE_404,
    RESPONSE_500,
    TAGS_CONTACT,
)
from ..models import Contact
from ..serializers import ContactResponseSerializer, ContactSerializer
from ..services import ContactService
from ..throttles import ContactsThrottle

logger = logging.getLogger("core.contact")


class ContactViewSet(BaseAPIViewSet):
    """API endpoint pour les soumissions de contact."""

    serializer_class = ContactSerializer
    throttle_classes = [ContactsThrottle]
    lookup_field = "pk"

    def get_permissions(self):
        """Anonyme pour create, admin explicite pour le reste."""
        if self.action == "create":
            return [AllowAnonymousCreate()]
        return [IsAdminOnly()]

    def _get_base_queryset(self):
        """Filtre les contacts selon les permissions.

        - Admin: voit tous les contacts
        - Anonymous: ne voit rien (create seulement)
        """
        user = self.request.user
        if user and user.is_authenticated and user.is_staff:
            return Contact.objects.all().order_by("-created_at")
        return Contact.objects.none()

    @swagger_auto_schema(
        operation_summary="Liste des soumissions",
        operation_description="Recupere la liste des soumissions de contact (admin uniquement).",
        responses={200: ContactSerializer(many=True), 401: RESPONSE_401, 403: RESPONSE_403},
        tags=TAGS_CONTACT,
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Liste les soumissions de contact (admin uniquement)."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Soumettre un formulaire",
        operation_description="Soumet un formulaire de contact.",
        request_body=ContactSerializer,
        responses={201: RESPONSE_201_CONTACT, 400: RESPONSE_400, 500: RESPONSE_500},
        tags=TAGS_CONTACT,
    )
    def create(self, request: Request, *_args: Any, **_kwargs: Any) -> Response:
        """Soumet un formulaire de contact.

        Les erreurs de validation (serializer) et de service (ServiceError)
        remontent au custom_exception_handler global qui les formate en
        {"errors": [{"code": "...", "message": "..."}]}.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ip_address = get_client_ip(request)
        reference_id = ContactService.submit_form(
            data=serializer.validated_data,
            ip_address=ip_address,
        )

        return self._build_success_response("Votre message a ete envoye avec succes.", reference_id)

    @swagger_auto_schema(
        operation_summary="Details d'une soumission",
        operation_description="Recupere les details d'une soumission de contact (admin uniquement).",
        responses={200: ContactSerializer(), 401: RESPONSE_401, 403: RESPONSE_403, 404: RESPONSE_404},
        tags=TAGS_CONTACT,
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Recupere les details d'une soumission (admin uniquement)."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Mettre a jour une soumission",
        operation_description="Met a jour une soumission de contact (admin uniquement).",
        request_body=ContactSerializer,
        responses={
            200: ContactSerializer(),
            400: RESPONSE_400,
            401: RESPONSE_401,
            403: RESPONSE_403,
            404: RESPONSE_404,
        },
        tags=TAGS_CONTACT,
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour une soumission (admin uniquement)."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Mettre a jour partiellement une soumission",
        operation_description="Met a jour partiellement une soumission de contact (admin uniquement).",
        request_body=ContactSerializer,
        responses={
            200: ContactSerializer(),
            400: RESPONSE_400,
            401: RESPONSE_401,
            403: RESPONSE_403,
            404: RESPONSE_404,
        },
        tags=TAGS_CONTACT,
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Met a jour partiellement une soumission (admin uniquement)."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Supprimer une soumission",
        operation_description="Supprime une soumission de contact (admin uniquement).",
        responses={204: RESPONSE_204, 401: RESPONSE_401, 403: RESPONSE_403, 404: RESPONSE_404},
        tags=TAGS_CONTACT,
    )
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Supprime une soumission (admin uniquement)."""
        return super().destroy(request, *args, **kwargs)

    def _build_success_response(self, message: str, reference_id: str) -> Response:
        """Construit une reponse de succes."""
        response_data = {
            "success": True,
            "message": message,
            "referenceId": reference_id,
        }
        response_serializer = ContactResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
