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
    """Protocol pour les classes ayant get_serializer_class."""

    def get_serializer_class(self) -> type[Serializer]: ...


class ViewSetProtocol(Protocol):
    """Protocol pour les methodes de ViewSet utilisees par les mixins."""

    request: Any
    kwargs: dict[str, Any]

    def get_queryset(self) -> QuerySet[Any]: ...
    def filter_queryset(self, queryset: QuerySet[Any]) -> QuerySet[Any]: ...
    def check_object_permissions(self, request: Any, obj: Any) -> None: ...


class SerializerByActionMixin:
    """Mixin pour selectionner le serializer selon l'action.

    Attributes:
        serializer_classes: Dict mapping action -> serializer class
        default_serializer_class: Serializer par defaut

    Usage:
        class MyViewSet(SerializerByActionMixin, viewsets.ModelViewSet):
            serializer_classes = {
                'list': MyListSerializer,
                'retrieve': MyDetailSerializer,
                'create': MyWriteSerializer,
                'update': MyWriteSerializer,
            }
            default_serializer_class = MyDetailSerializer
    """

    serializer_classes: ClassVar[dict[str, type[Serializer]]] = {}
    default_serializer_class: ClassVar[type[Serializer] | None] = None

    def get_serializer_class(self) -> type[Serializer]:
        """Retourne le serializer selon l'action courante."""
        action = getattr(self, "action", None)
        if action and action in self.serializer_classes:
            return self.serializer_classes[action]

        # Grouper les actions similaires
        if action in ("create", "update", "partial_update") and "write" in self.serializer_classes:
            return self.serializer_classes["write"]

        if action in ("list",) and "list" in self.serializer_classes:
            return self.serializer_classes["list"]

        if action in ("retrieve",) and "detail" in self.serializer_classes:
            return self.serializer_classes["detail"]

        if self.default_serializer_class:
            return self.default_serializer_class

        # Call parent's get_serializer_class - relies on MRO with ViewSet
        parent = cast(HasGetSerializerClass, super())
        return parent.get_serializer_class()


class SlugOrPkLookupMixin:
    """Mixin pour lookup par slug ou pk.

    Permet d'acceder aux objets via /resource/slug/ ou /resource/123/
    Designed to be used with ViewSet (methods provided via MRO).

    Lookup strategy per module:
        - slug (via ce mixin): articles, projects, stacks
          → ces modeles ont un champ slug unique pour les URLs publiques
        - pk (lookup_field="pk"): experiences, contact
          → ces modeles n'ont pas de slug dans leur modele
    """

    lookup_field: str = "slug"
    lookup_url_kwarg: str | None = None
    kwargs: dict[str, str]
    request: Request

    # Provided by ViewSet via MRO — declared here for type checking only
    if TYPE_CHECKING:

        def get_queryset(self) -> QuerySet[Any]: ...
        def filter_queryset(self, queryset: QuerySet[Any]) -> QuerySet[Any]: ...
        def check_object_permissions(self, request: Any, obj: Any) -> None: ...

    def get_object(self) -> Model:
        """Recupere l'objet par slug ou pk."""
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs.get(lookup_url_kwarg)

        # Essayer d'abord par slug
        filter_kwargs = {self.lookup_field: lookup_value}
        obj = queryset.filter(**filter_kwargs).first()

        # Si pas trouve et que c'est un nombre, essayer par pk
        if obj is None and lookup_value and lookup_value.isdigit():
            obj = queryset.filter(pk=int(lookup_value)).first()

        if obj is None:
            from utils.exceptions.service import NotFoundError

            raise NotFoundError(f"Objet non trouve: {lookup_value}")

        # Verifier les permissions
        self.check_object_permissions(self.request, obj)
        return obj


class AdminWritePermissionMixin:
    """Mixin pour permissions: lecture publique, ecriture admin.

    Usage:
        class MyViewSet(AdminWritePermissionMixin, viewsets.ModelViewSet):
            pass
    """

    action: str

    def get_permissions(self) -> list[permissions.BasePermission]:
        """Retourne les permissions selon l'action."""
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class LoggingMixin:
    """Mixin pour ajouter du logging aux actions CRUD.

    Ajoute automatiquement des logs pour create, update, destroy.
    """

    request: Request

    def perform_create(self, serializer: Serializer) -> None:
        """Log la creation d'un objet."""
        instance = serializer.save()
        logger.info(
            "[CREATE] %s id=%s by user=%s",
            instance.__class__.__name__,
            instance.pk,
            getattr(self.request.user, "id", "anonymous"),
        )

    def perform_update(self, serializer: Serializer) -> None:
        """Log la mise a jour d'un objet."""
        instance = serializer.save()
        logger.info(
            "[UPDATE] %s id=%s by user=%s",
            instance.__class__.__name__,
            instance.pk,
            getattr(self.request.user, "id", "anonymous"),
        )

    def perform_destroy(self, instance: Model) -> None:
        """Log la suppression d'un objet."""
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
    """ViewSet de base avec toutes les fonctionnalites communes.

    Combine:
    - Selection automatique du serializer par action
    - Lookup par slug ou pk
    - Permissions admin pour ecriture
    - Logging automatique des actions CRUD
    - Guard automatique pour swagger_fake_view

    Usage:
        class ArticleViewSet(BaseAPIViewSet):
            queryset = Article.objects.all()
            serializer_classes = {
                'list': ArticleListSerializer,
                'detail': ArticleDetailSerializer,
                'write': ArticleWriteSerializer,
            }
            default_serializer_class = ArticleDetailSerializer

            def _get_base_queryset(self):
                return Article.objects.with_related()
    """

    def get_queryset(self) -> QuerySet[Any]:
        """Retourne le queryset avec guard swagger_fake_view.

        Les sous-classes doivent surcharger _get_base_queryset()
        au lieu de get_queryset() pour beneficier du guard automatique.
        """
        if getattr(self, "swagger_fake_view", False):
            if self.queryset is None:
                return QuerySet(model=Model).none()
            return self.queryset.model.objects.none()
        return self._get_base_queryset()

    def _get_base_queryset(self) -> QuerySet[Any]:
        """Retourne le queryset de base. A surcharger dans les sous-classes."""
        return super().get_queryset()

    def paginated_response(
        self,
        queryset: QuerySet[Any],
        serializer_class: type[Serializer] | None = None,
    ) -> Response:
        """Pagine un queryset et retourne une reponse serialisee.

        Args:
            queryset: QuerySet a paginer.
            serializer_class: Serializer a utiliser. Si None, utilise
                le serializer de l'action courante.
        """
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
        """Ecrit avec le serializer d'action et repond avec un autre serializer.

        Utile quand on veut valider avec un WriteSerializer mais repondre
        avec un ListSerializer (ex: ProjectViewSet).

        Args:
            request: La requete HTTP.
            response_serializer_class: Serializer pour la reponse.
            instance: Instance existante (update) ou None (create).
            partial: Mise a jour partielle.
        """
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
    """ViewSet en lecture seule avec fonctionnalites communes."""

    permission_classes = [permissions.AllowAny]
