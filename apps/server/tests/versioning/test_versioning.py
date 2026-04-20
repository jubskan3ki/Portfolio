"""Tests pour le module versioning : soft delete + snapshots + restore."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from core.articles.models import Article
from core.versioning.models import Version
from core.versioning.services import (
    UnknownModelError,
    VersionNotFoundError,
    restore_version,
)

from ..factories import ArticleFactory

VERSIONS_URL = "/api/versioning/versions/"
RESTORE_URL = "/api/versioning/restore/"
TRASH_URL = "/api/versioning/trashed/"
UNTRASH_URL = "/api/versioning/untrash/"


@pytest.mark.django_db
class TestSoftDeleteMixin:
    """Soft-delete applique a Article."""

    def test_soft_delete_sets_deleted_at(self) -> None:
        article = ArticleFactory(title="ToDelete")
        article.soft_delete()
        article.refresh_from_db()
        assert article.deleted_at is not None

    def test_soft_deleted_excluded_from_published(self) -> None:
        article = ArticleFactory(title="SoftDel")
        article.soft_delete()
        assert not Article.objects.published().filter(pk=article.pk).exists()

    def test_soft_deleted_visible_via_all_objects(self) -> None:
        article = ArticleFactory(title="StillThere")
        article.soft_delete()
        assert Article.all_objects.filter(pk=article.pk).exists()

    def test_restore_resets_deleted_at(self) -> None:
        article = ArticleFactory(title="Restore")
        article.soft_delete()
        article.restore()
        article.refresh_from_db()
        assert article.deleted_at is None


@pytest.mark.django_db
class TestVersionSnapshot:
    """Les snapshots sont crees automatiquement via signal post_save."""

    def test_create_article_creates_version(self) -> None:
        Version.objects.filter(content_type="Article").delete()
        article = ArticleFactory(title="NewPost")
        versions = Version.objects.filter(content_type="Article", object_id=str(article.pk))
        assert versions.count() >= 1

    def test_update_article_increments_version_number(self) -> None:
        article = ArticleFactory(title="Original")
        Version.objects.filter(content_type="Article", object_id=str(article.pk)).delete()
        article.title = "Edited"
        article.save()
        article.title = "EditedAgain"
        article.save()
        versions = list(
            Version.objects.filter(content_type="Article", object_id=str(article.pk)).order_by("version_number")
        )
        assert len(versions) >= 2
        assert versions[-1].version_number > versions[0].version_number

    def test_snapshot_contains_title(self) -> None:
        article = ArticleFactory(title="Snapshotted")
        v = (
            Version.objects.filter(content_type="Article", object_id=str(article.pk))
            .order_by("-version_number")
            .first()
        )
        assert v is not None
        assert v.snapshot.get("title") == "Snapshotted"


@pytest.mark.django_db
class TestRestoreService:
    """restore_version remonte a l'etat d'une version precedente."""

    def test_restore_applies_snapshot(self) -> None:
        article = ArticleFactory(title="V1")
        v1 = (
            Version.objects.filter(content_type="Article", object_id=str(article.pk))
            .order_by("-version_number")
            .first()
        )
        article.title = "V2"
        article.save()
        article.title = "V3"
        article.save()

        restore_version(v1.id)

        article.refresh_from_db()
        assert article.title == "V1"

    def test_restore_unknown_version_raises(self) -> None:
        with pytest.raises(VersionNotFoundError):
            restore_version(999_999)

    def test_restore_unknown_model_raises(self) -> None:
        v = Version.objects.create(content_type="DoesNotExist", object_id="1", version_number=1, snapshot={})
        with pytest.raises(UnknownModelError):
            restore_version(v.id)


@pytest.mark.django_db
class TestVersionListEndpoint:
    """GET /api/versioning/versions/."""

    def test_admin_can_list_versions(self, authenticated_client: APIClient) -> None:
        article = ArticleFactory(title="Listed")
        response = cast(
            Response,
            authenticated_client.get(f"{VERSIONS_URL}?model=Article&object_id={article.pk}"),
        )
        assert response.status_code == status.HTTP_200_OK
        data = cast(list[dict[str, Any]], response.data)
        assert len(data) >= 1

    def test_requires_model_param(self, authenticated_client: APIClient) -> None:
        response = cast(Response, authenticated_client.get(f"{VERSIONS_URL}?object_id=1"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_requires_object_id_param(self, authenticated_client: APIClient) -> None:
        response = cast(Response, authenticated_client.get(f"{VERSIONS_URL}?model=Article"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_anon_forbidden(self, api_client: APIClient) -> None:
        response = cast(Response, api_client.get(f"{VERSIONS_URL}?model=Article&object_id=1"))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_regular_user_forbidden(self, user_client: APIClient) -> None:
        response = cast(Response, user_client.get(f"{VERSIONS_URL}?model=Article&object_id=1"))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


@pytest.mark.django_db
class TestRestoreEndpoint:
    """POST /api/versioning/restore/<version_id>/."""

    def test_admin_can_restore(self, authenticated_client: APIClient) -> None:
        article = ArticleFactory(title="V1")
        v1 = (
            Version.objects.filter(content_type="Article", object_id=str(article.pk))
            .order_by("-version_number")
            .first()
        )
        article.title = "V2"
        article.save()

        response = cast(Response, authenticated_client.post(f"{RESTORE_URL}{v1.id}/"))

        assert response.status_code == status.HTTP_200_OK
        article.refresh_from_db()
        assert article.title == "V1"

    def test_404_for_unknown_version(self, authenticated_client: APIClient) -> None:
        response = cast(Response, authenticated_client.post(f"{RESTORE_URL}999999/"))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_anon_forbidden(self, api_client: APIClient) -> None:
        response = cast(Response, api_client.post(f"{RESTORE_URL}1/"))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


@pytest.mark.django_db
class TestTrashEndpoints:
    """GET /api/versioning/trashed/ + POST /api/versioning/untrash/."""

    def test_list_trashed(self, authenticated_client: APIClient) -> None:
        a = ArticleFactory(title="Trashed")
        a.soft_delete()
        response = cast(Response, authenticated_client.get(f"{TRASH_URL}?model=Article"))
        assert response.status_code == status.HTTP_200_OK
        pks = [row["pk"] for row in cast(list[dict[str, Any]], response.data)]
        assert a.pk in pks

    def test_untrash_restores(self, authenticated_client: APIClient) -> None:
        a = ArticleFactory(title="WillRestore")
        a.soft_delete()
        response = cast(
            Response,
            authenticated_client.post(f"{UNTRASH_URL}?model=Article&object_id={a.pk}"),
        )
        assert response.status_code == status.HTTP_200_OK
        a.refresh_from_db()
        assert a.deleted_at is None

    def test_trashed_requires_model(self, authenticated_client: APIClient) -> None:
        response = cast(Response, authenticated_client.get(TRASH_URL))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_trashed_unknown_model_400(self, authenticated_client: APIClient) -> None:
        response = cast(Response, authenticated_client.get(f"{TRASH_URL}?model=NopeModel"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_untrash_not_found(self, authenticated_client: APIClient) -> None:
        response = cast(
            Response,
            authenticated_client.post(f"{UNTRASH_URL}?model=Article&object_id=999999"),
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_trash_anon_forbidden(self, api_client: APIClient) -> None:
        response = cast(Response, api_client.get(f"{TRASH_URL}?model=Article"))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
