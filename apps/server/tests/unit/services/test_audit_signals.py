"""Tests unitaires pour les signaux d'audit."""

from __future__ import annotations

import pytest

from core.audit.signals import (
    clear_audit_context,
    get_audit_context,
    set_audit_context,
)
from tests.factories import (
    ArticleCategoryFactory,
    ArticleFactory,
    StackCategoryFactory,
    StackFactory,
)


class TestAuditContext:
    """Tests pour la gestion du contexte d'audit thread-local."""

    def test_set_and_get_context(self) -> None:
        """Definir et recuperer le contexte fonctionne."""
        set_audit_context(
            ip_address="192.168.1.1",
            user_agent="TestAgent",
            correlation_id="test-123",
        )

        ctx = get_audit_context()

        assert ctx["ip_address"] == "192.168.1.1"
        assert ctx["user_agent"] == "TestAgent"
        assert ctx["correlation_id"] == "test-123"

    def test_clear_context(self) -> None:
        """Nettoyer le contexte remet les valeurs par defaut."""
        set_audit_context(ip_address="192.168.1.1")

        clear_audit_context()
        ctx = get_audit_context()

        assert ctx["ip_address"] is None

    def test_default_context_values(self) -> None:
        """Le contexte par defaut a des valeurs vides."""
        clear_audit_context()
        ctx = get_audit_context()

        assert ctx["user"] is None
        assert ctx["ip_address"] is None
        assert ctx["user_agent"] == ""
        assert ctx["correlation_id"] == ""


@pytest.mark.django_db
class TestAuditSignals:
    """Tests pour les signaux d'audit (creation/modification/suppression)."""

    def test_create_logs_audit(self) -> None:
        """La creation d'un modele audite genere un log."""
        from core.audit.models import AuditLog

        initial_count = AuditLog.objects.count()
        category = ArticleCategoryFactory()
        ArticleFactory(category=category)

        assert AuditLog.objects.count() > initial_count

    def test_update_logs_audit(self) -> None:
        """La modification d'un modele audite genere un log."""
        from core.audit.models import AuditLog

        category = StackCategoryFactory()
        stack = StackFactory(category=category, name="Original")
        count_before = AuditLog.objects.count()

        stack.name = "Modified"
        stack.save()

        assert AuditLog.objects.count() > count_before

    def test_delete_logs_audit(self) -> None:
        """La suppression d'un modele audite genere un log."""
        from core.audit.models import AuditLog

        category = StackCategoryFactory()
        stack = StackFactory(category=category)
        count_before = AuditLog.objects.count()

        stack.delete()

        assert AuditLog.objects.count() > count_before
