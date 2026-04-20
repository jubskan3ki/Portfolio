"""Mixins centralises pour les API ViewSets."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, ClassVar, Protocol, cast

from django.db.models import Model, QuerySet
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer

if TYPE_CHECKING:
    from rest_framework.request import Request

logger = logging.getLogger(__name__)


class HasGetSerializerClass(Protocol):
    def get_serializer_class(self) -> type[Serializer]: ...


class ViewSetProtocol(Protocol):
    request: Any
    kwargs: dict[str, Any]

    def get_queryset(self) -> QuerySet[Any]: ...
    def filter_queryset(self, queryset: QuerySet[Any]) -> QuerySet[Any]: ...
    def check_object_permissions(self, request: Any, obj: Any) -> None: ...


class SerializerByActionMixin:
    """Selectionne le serializer selon action via serializer_classes dict."""

    serializer_classes: ClassVar[dict[str, type[Serializer]]] = {}
    default_serializer_class: ClassVar[type[Serializer] | None] = None

    def get_serializer_class(self) -> type[Serializer]:
        action = getattr(self, "action", None)
        if action and action in self.serializer_classes:
            return self.serializer_classes[action]

        # Alias d'actions similaires
        if action in ("create", "update", "partial_update") and "write" in self.serializer_classes:
            return self.serializer_classes["write"]

        if action in ("list",) and "list" in self.serializer_classes:
            return self.serializer_classes["list"]

        if action in ("retrieve",) and "detail" in self.serializer_classes:
            return self.serializer_classes["detail"]

        if self.default_serializer_class:
            return self.default_serializer_class

        parent = cast(HasGetSerializerClass, super())
        return parent.get_serializer_class()


class SlugOrPkLookupMixin:
    """Lookup par slug (defaut), fallback sur pk si la valeur est numerique.

    Modeles avec slug : articles, projects, stacks. Sans slug : experiences, contact (lookup_field='pk').
    """

    lookup_field: str = "slug"
    lookup_url_kwarg: str | None = None
    kwargs: dict[str, str]
    request: Request

    if TYPE_CHECKING:

        def get_queryset(self) -> QuerySet[Any]: ...
        def filter_queryset(self, queryset: QuerySet[Any]) -> QuerySet[Any]: ...
        def check_object_permissions(self, request: Any, obj: Any) -> None: ...

    def get_object(self) -> Model:
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs.get(lookup_url_kwarg)

        filter_kwargs = {self.lookup_field: lookup_value}
        obj = queryset.filter(**filter_kwargs).first()

        if obj is None and lookup_value and lookup_value.isdigit():
            obj = queryset.filter(pk=int(lookup_value)).first()

        if obj is None:
            from utils.exceptions.service import NotFoundError

            raise NotFoundError(f"Objet non trouve: {lookup_value}")

        self.check_object_permissions(self.request, obj)
        return obj


class AdminWritePermissionMixin:
    """Lecture publique, ecriture admin."""

    action: str

    def get_permissions(self) -> list[permissions.BasePermission]:
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class LoggingMixin:
    """Logs automatiques sur create/update/destroy."""

    request: Request

    def perform_create(self, serializer: Serializer) -> None:
        instance = serializer.save()
        logger.info(
            "[CREATE] %s id=%s by user=%s",
            instance.__class__.__name__,
            instance.pk,
            getattr(self.request.user, "id", "anonymous"),
        )

    def perform_update(self, serializer: Serializer) -> None:
        instance = serializer.save()
        logger.info(
            "[UPDATE] %s id=%s by user=%s",
            instance.__class__.__name__,
            instance.pk,
            getattr(self.request.user, "id", "anonymous"),
        )

    def perform_destroy(self, instance: Model) -> None:
        model_name = instance.__class__.__name__
        instance_pk = instance.pk
        instance.delete()
        logger.info(
            "[DELETE] %s id=%s by user=%s",
            model_name,
            instance_pk,
            getattr(self.request.user, "id", "anonymous"),
        )


class BaseAPIViewSet(
    SerializerByActionMixin,
    SlugOrPkLookupMixin,
    AdminWritePermissionMixin,
    LoggingMixin,
    viewsets.ModelViewSet,
):
    """ViewSet de base. Sous-classes surchargent _get_base_queryset() (guard swagger_fake_view auto)."""

    def get_queryset(self) -> QuerySet[Any]:
        if getattr(self, "swagger_fake_view", False):
            if self.queryset is not None:
                return self.queryset.model.objects.none()
            # Fallback : derive model depuis serializer.Meta
            serializer_class = getattr(self, "serializer_class", None)
            if serializer_class is not None:
                meta = getattr(serializer_class, "Meta", None)
                model = getattr(meta, "model", None) if meta else None
                if model is not None:
                    return model.objects.none()
            return QuerySet()
        return self._get_base_queryset()

    def _get_base_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()

    def paginated_response(
        self,
        queryset: QuerySet[Any],
        serializer_class: type[Serializer] | None = None,
    ) -> Response:
        cls = serializer_class or self.get_serializer_class()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = cls(page, many=True, context={"request": self.request})
            return self.get_paginated_response(serializer.data)
        serializer = cls(queryset, many=True, context={"request": self.request})
        return Response(serializer.data)

    def write_with_response_serializer(
        self,
        request: Request,
        response_serializer_class: type[Serializer],
        *,
        instance: Model | None = None,
        partial: bool = False,
    ) -> Response:
        """Valide avec WriteSerializer, repond avec un autre serializer (ex: ListSerializer)."""
        write_serializer = cast(
            Serializer,
            self.get_serializer(instance, data=request.data, partial=partial),
        )
        write_serializer.is_valid(raise_exception=True)
        if instance is None:
            self.perform_create(write_serializer)
            status_code = 201
        else:
            self.perform_update(write_serializer)
            status_code = 200
        response_serializer = response_serializer_class(write_serializer.instance, context={"request": request})
        return Response(response_serializer.data, status=status_code)


class ReadOnlyAPIViewSet(
    SerializerByActionMixin,
    SlugOrPkLookupMixin,
    viewsets.ReadOnlyModelViewSet,
):
    permission_classes = [permissions.AllowAny]
