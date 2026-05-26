"""Tests pour les extensions PR #2 : timeline, stats, cleanup task, admin diff."""

from __future__ import annotations

from datetime import timedelta
from typing import Any, cast

import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from core.audit.models import AuditLog
from core.audit.services import compute_stats, get_object_timeline
from core.audit.signals import AUDITED_MODELS
from core.audit.tasks import cleanup_old_audit_logs

from ..factories import ArticleFactory, AuditLogFactory

TIMELINE_URL = "/api/audit/logs/timeline/"
STATS_URL = "/api/audit/stats/"


@pytest.mark.django_db
class TestAuditTimelineEndpoint:
    """GET /api/audit/logs/timeline/?model=Article&id=<id>."""

    def test_returns_timeline_for_object(self, authenticated_client: APIClient) -> None:
        AuditLogFactory(action="create", model_name="Article", object_id="42")
        AuditLogFactory(action="update", model_name="Article", object_id="42")
        AuditLogFactory(action="create", model_name="Article", object_id="99")
        response = cast(
            Response,
            authenticated_client.get(f"{TIMELINE_URL}?model=Article&id=42"),
        )
        assert response.status_code == status.HTTP_200_OK
        logs = cast(list[dict[str, Any]], response.data)
        assert len(logs) == 2
        assert all(log["object_id"] == "42" for log in logs)

    def test_requires_model_param(self, authenticated_client: APIClient) -> None:
        response = cast(Response, authenticated_client.get(f"{TIMELINE_URL}?id=42"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_requires_id_param(self, authenticated_client: APIClient) -> None:
        response = cast(Response, authenticated_client.get(f"{TIMELINE_URL}?model=Article"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_anon_forbidden(self, api_client: APIClient) -> None:
        response = cast(Response, api_client.get(f"{TIMELINE_URL}?model=Article&id=1"))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_empty_when_no_logs(self, authenticated_client: APIClient) -> None:
        response = cast(
            Response,
            authenticated_client.get(f"{TIMELINE_URL}?model=Article&id=9999"),
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []


@pytest.mark.django_db
class TestAuditStatsEndpoint:
    """GET /api/audit/stats/."""

    def test_returns_stats_shape(self, authenticated_client: APIClient) -> None:
        AuditLogFactory(action="create", model_name="Article")
        AuditLogFactory(action="update", model_name="Article")
        AuditLogFactory(action="delete", model_name="Project")
        response = cast(Response, authenticated_client.get(STATS_URL))
        assert response.status_code == status.HTTP_200_OK
        data = cast(dict[str, Any], response.data)
        for key in ("window_days", "total", "by_action", "top_models", "top_users", "activity_per_day"):
            assert key in data

    def test_total_counts_correctly(self, authenticated_client: APIClient) -> None:
        for _ in range(5):
            AuditLogFactory(action="create", model_name="Article")
        response = cast(Response, authenticated_client.get(STATS_URL))
        assert cast(dict[str, Any], response.data)["total"] >= 5

    def test_window_days_param(self, authenticated_client: APIClient) -> None:
        AuditLogFactory(action="create", model_name="Article")
        response = cast(Response, authenticated_client.get(f"{STATS_URL}?window_days=7"))
        assert response.status_code == status.HTTP_200_OK
        assert cast(dict[str, Any], response.data)["window_days"] == 7

    def test_rejects_zero_window(self, authenticated_client: APIClient) -> None:
        response = cast(Response, authenticated_client.get(f"{STATS_URL}?window_days=0"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_rejects_negative_window(self, authenticated_client: APIClient) -> None:
        response = cast(Response, authenticated_client.get(f"{STATS_URL}?window_days=-1"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_rejects_non_integer(self, authenticated_client: APIClient) -> None:
        response = cast(Response, authenticated_client.get(f"{STATS_URL}?window_days=abc"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_anon_forbidden(self, api_client: APIClient) -> None:
        response = cast(Response, api_client.get(STATS_URL))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_regular_user_forbidden(self, user_client: APIClient) -> None:
        response = cast(Response, user_client.get(STATS_URL))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


@pytest.mark.django_db
class TestAuditServices:
    """Tests unitaires pour core.audit.services."""

    def test_compute_stats_groups_by_action(self) -> None:
        AuditLogFactory(action="create")
        AuditLogFactory(action="create")
        AuditLogFactory(action="update")
        stats = compute_stats()
        assert stats["by_action"]["create"] == 2
        assert stats["by_action"]["update"] == 1

    def test_compute_stats_excludes_old_logs(self) -> None:
        AuditLogFactory(timestamp=timezone.now() - timedelta(days=365))
        AuditLogFactory()
        stats = compute_stats(window_days=30)
        assert stats["total"] == 1

    def test_top_models_sorted_desc(self) -> None:
        for _ in range(5):
            AuditLogFactory(model_name="Article")
        for _ in range(2):
            AuditLogFactory(model_name="Project")
        stats = compute_stats()
        models = stats["top_models"]
        assert models[0]["model_name"] == "Article"
        assert models[0]["count"] >= models[1]["count"]

    def test_top_users_excludes_anonymous(self, admin_user) -> None:
        AuditLogFactory(user=admin_user.user)
        AuditLogFactory(user=None)
        stats = compute_stats()
        emails = [u["user__email"] for u in stats["top_users"]]
        assert admin_user.user.email in emails
        assert None not in emails

    def test_get_object_timeline_returns_matching_logs_desc(self) -> None:
        AuditLogFactory(model_name="Stack", object_id="5", action="create")
        AuditLogFactory(model_name="Stack", object_id="5", action="update")
        AuditLogFactory(model_name="Stack", object_id="9", action="create")
        logs = get_object_timeline("Stack", "5")
        assert len(logs) == 2
        assert logs[0].timestamp >= logs[1].timestamp


@pytest.mark.django_db
class TestAuditCleanupTask:
    """Tests Celery task cleanup_old_audit_logs."""

    def test_deletes_logs_older_than_retention(self) -> None:
        fresh = AuditLogFactory()
        old = AuditLogFactory(timestamp=timezone.now() - timedelta(days=365))
        result = cleanup_old_audit_logs(days=180)
        assert result["deleted_count"] == 1
        assert AuditLog.objects.filter(id=fresh.id).exists()
        assert not AuditLog.objects.filter(id=old.id).exists()

    def test_uses_default_retention_when_none(self) -> None:
        result = cleanup_old_audit_logs(days=None)
        assert "retention_days" in result
        assert result["retention_days"] > 0

    def test_respects_custom_days(self) -> None:
        AuditLogFactory(timestamp=timezone.now() - timedelta(days=10))
        result = cleanup_old_audit_logs(days=5)
        assert result["deleted_count"] == 1


@pytest.mark.django_db
class TestAuditSignalsExtended:
    """Les nouveaux modeles ajoutes a AUDITED_MODELS sont bien audites."""

    def test_category_creation_is_audited(self) -> None:
        from core.articles.models import Category

        existing = AuditLog.objects.filter(model_name="Category").count()
        Category.objects.create(name="NewCat", slug="newcat")
        after = AuditLog.objects.filter(model_name="Category", action="create").count()
        assert after >= existing + 1

    def test_audited_models_contains_new_entries(self) -> None:
        for name in ("Category", "Tag", "ProjectCategory", "ProjectStatus", "StackCategory", "ExperienceType"):
            assert name in AUDITED_MODELS


@pytest.mark.django_db
class TestAuditSignalChangesTracking:
    """Le signal _log_save enregistre les diffs avant/apres."""

    def test_update_records_changes(self) -> None:
        article = ArticleFactory(title="Original")
        AuditLog.objects.filter(model_name="Article", action="update").delete()
        article.title = "Modified"
        article.save()
        log = AuditLog.objects.filter(model_name="Article", object_id=str(article.pk), action="update").first()
        assert log is not None
        assert "title" in log.changes
        assert log.changes["title"]["old"] == "Original"
        assert log.changes["title"]["new"] == "Modified"
