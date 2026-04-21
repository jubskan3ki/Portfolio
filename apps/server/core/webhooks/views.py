"""Vues pour le module webhooks."""

import uuid
from typing import Any, cast

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from utils.api import BaseAPIViewSet, ReadOnlyAPIViewSet

from .models import Webhook, WebhookDelivery, WebhookEventType
from .serializers import (
    WebhookDeliverySerializer,
    WebhookEventTypesSerializer,
    WebhookSerializer,
)
from .services import WebhookDispatcher
from .throttles import WebhooksThrottle


class WebhookViewSet(BaseAPIViewSet):
    """ViewSet pour la gestion des webhooks."""

    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [WebhooksThrottle]
    lookup_field = "pk"

    def get_permissions(self):
        """Toutes les actions webhook necessitent un admin."""
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        """Associe le webhook a l'utilisateur courant."""
        serializer.save(created_by=self.request.user)

    def _get_base_queryset(self):
        """Retourne les webhooks de l'utilisateur courant."""
        return Webhook.objects.filter(created_by=self.request.user)

    @action(detail=False, methods=["get"])
    def event_types(self, _request: Request) -> Response:
        """Liste les types d'evenements disponibles."""
        events = [{"value": choice[0], "label": choice[1]} for choice in WebhookEventType.choices]
        serializer = WebhookEventTypesSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def test(self, _request: Request, **_kwargs: Any) -> Response:
        """Teste un webhook en envoyant un evenement de test."""
        webhook = cast(Webhook, self.get_object())

        test_payload = {
            "id": 0,
            "message": "Ceci est un evenement de test",
            "webhook_id": webhook.id,
        }

        # Create and send delivery directly to this webhook | bypass dispatch()
        # because "test.ping" is not a real WebhookEventType and for_event()
        # would never match.
        first_event = webhook.events[0] if webhook.events else "article.created"
        delivery = WebhookDispatcher._create_delivery(webhook, first_event, test_payload, uuid.uuid4())
        WebhookDispatcher.send_delivery(delivery)

        return Response(
            {
                "success": delivery.status == WebhookDelivery.Status.SUCCESS,
                "status_code": delivery.response_status,
                "duration_ms": delivery.duration_ms,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def toggle(self, _request: Request, **_kwargs: Any) -> Response:
        """Active/desactive un webhook."""
        webhook = cast(Webhook, self.get_object())
        is_active = WebhookDispatcher.toggle(webhook)

        return Response(
            {"is_active": is_active},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"])
    def deliveries(self, _request: Request, **_kwargs: Any) -> Response:
        """Liste les livraisons d'un webhook avec pagination."""
        webhook = cast(Webhook, self.get_object())
        queryset = webhook.deliveries.all().order_by("-created_at")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = WebhookDeliverySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = WebhookDeliverySerializer(queryset, many=True)
        return Response(serializer.data)


class WebhookDeliveryViewSet(ReadOnlyAPIViewSet):
    """ViewSet en lecture seule pour l'historique des livraisons."""

    serializer_class = WebhookDeliverySerializer
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [WebhooksThrottle]

    def get_queryset(self):
        """Retourne les livraisons des webhooks de l'utilisateur."""
        return WebhookDelivery.objects.select_related("webhook").filter(webhook__created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def retry(self, _request: Request, **_kwargs: Any) -> Response:
        """Retente une livraison echouee."""
        delivery = cast(WebhookDelivery, self.get_object())

        if delivery.status not in [
            WebhookDelivery.Status.FAILED,
            WebhookDelivery.Status.RETRYING,
        ]:
            return Response(
                {"error": "Seules les livraisons echouees peuvent etre retentees"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        WebhookDispatcher.send_delivery(delivery)

        return Response(
            {
                "status": delivery.status,
                "response_status": delivery.response_status,
            },
            status=status.HTTP_200_OK,
        )
