"""Tests pour le dry-run d'import (PR #6)."""

from __future__ import annotations

import json
from typing import Any, cast

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from core.articles.models import Article
from core.transfer.services.dry_run import dry_run_import

from ..factories import ArticleCategoryFactory, ArticleFactory


def _json_file(payload: list[dict[str, Any]], name: str = "data.json") -> SimpleUploadedFile:
    content = json.dumps(payload).encode("utf-8")
    return SimpleUploadedFile(name, content, content_type="application/json")


@pytest.mark.django_db
class TestDryRunService:
    """dry_run_import ne persiste RIEN et produit un diff correct."""

    def test_unknown_module_raises(self) -> None:
        file = _json_file([{"title": "t", "slug": "s"}])
        with pytest.raises(ValueError):
            dry_run_import(file, "unknown_module")

    def test_classifies_creates(self) -> None:
        cat = ArticleCategoryFactory(name="CatExists")
        file = _json_file(
            [
                {"title": "Brand New", "slug": "brand-new", "excerpt": "Ex", "category": cat.name},
            ]
        )
        result = dry_run_import(file, "articles")
        assert result["summary"]["create"] == 1
        assert result["summary"]["update"] == 0

    def test_classifies_updates_with_diff(self) -> None:
        article = ArticleFactory(title="Original", slug="unique-update-test", excerpt="old")
        file = _json_file(
            [
                {"title": "Changed Title", "slug": article.slug, "excerpt": "old"},
            ]
        )
        result = dry_run_import(file, "articles")
        updates = result["would_update"]
        assert len(updates) == 1
        assert "title" in updates[0]["diff"]
        assert updates[0]["diff"]["title"]["current"] == "Original"
        assert updates[0]["diff"]["title"]["new"] == "Changed Title"

    def test_does_not_persist(self) -> None:
        count_before = Article.objects.count()
        file = _json_file(
            [
                {"title": "ShouldNotPersist", "slug": "should-not-persist", "excerpt": "x"},
            ]
        )
        dry_run_import(file, "articles")
        count_after = Article.objects.count()
        assert count_before == count_after

    def test_skip_records_with_missing_unique_field(self) -> None:
        file = _json_file([{"title": "NoSlug"}])
        result = dry_run_import(file, "articles")
        assert result["summary"]["skip"] >= 1

    def test_identical_record_is_skipped_not_updated(self) -> None:
        article = ArticleFactory(title="Same", slug="identical-slug-test", excerpt="ex")
        file = _json_file([{"slug": article.slug, "title": article.title, "excerpt": article.excerpt}])
        result = dry_run_import(file, "articles")
        assert result["summary"]["update"] == 0
        assert result["summary"]["skip"] >= 1


@pytest.mark.django_db
class TestDryRunEndpoint:
    """POST /api/transfer/import/dry-run/<module>/."""

    URL = "/api/transfer/import/dry-run/articles/"

    def test_admin_can_call_dry_run(self, authenticated_client: APIClient) -> None:
        file = _json_file([{"title": "T", "slug": "t", "excerpt": "e"}])
        response = cast(
            Response,
            authenticated_client.post(self.URL, {"file": file}, format="multipart"),
        )
        assert response.status_code == status.HTTP_200_OK
        data = cast(dict[str, Any], response.data)
        assert "summary" in data
        assert "would_create" in data

    def test_missing_file_returns_400(self, authenticated_client: APIClient) -> None:
        response = cast(Response, authenticated_client.post(self.URL, {}, format="multipart"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_anon_forbidden(self, api_client: APIClient) -> None:
        file = _json_file([{"title": "T", "slug": "t"}])
        response = cast(Response, api_client.post(self.URL, {"file": file}, format="multipart"))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_invalid_extension_rejected(self, authenticated_client: APIClient) -> None:
        bad = SimpleUploadedFile("data.txt", b"hello", content_type="text/plain")
        response = cast(
            Response,
            authenticated_client.post(self.URL, {"file": bad}, format="multipart"),
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unknown_module_returns_400(self, authenticated_client: APIClient) -> None:
        file = _json_file([{"title": "T", "slug": "t"}])
        response = cast(
            Response,
            authenticated_client.post("/api/transfer/import/dry-run/unknown/", {"file": file}, format="multipart"),
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
