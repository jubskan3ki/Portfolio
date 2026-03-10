"""Tests pour les logs d'audit."""

from __future__ import annotations

from typing import cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestAuditLogList:
    """Tests endpoint GET /api/audit/ (admin uniquement)."""

    URL = "/api/audit/logs/"

    def test_list_audit_logs_admin(self, authenticated_client: APIClient) -> None:
        """Admin peut lister les logs d'audit."""
        response = cast(Response, authenticated_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK

    def test_list_audit_logs_anonymous_forbidden(self, api_client: APIClient) -> None:
        """Utilisateur anonyme ne peut pas lister les logs."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_list_audit_logs_regular_user_forbidden(
        self,
        user_client: APIClient,
    ) -> None:
        """Utilisateur regulier ne peut pas lister les logs."""
        response = cast(Response, user_client.get(self.URL))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestAuditLogFiltering:
    """Tests filtrage des logs d'audit."""

    URL = "/api/audit/logs/"

    def test_filter_by_action(self, authenticated_client: APIClient) -> None:
        """Filtrage par action fonctionne."""
        response = cast(Response, authenticated_client.get(f"{self.URL}?action=create"))

        assert response.status_code == status.HTTP_200_OK

    def test_filter_by_model(self, authenticated_client: APIClient) -> None:
        """Filtrage par modele fonctionne."""
        response = cast(Response, authenticated_client.get(f"{self.URL}?model_name=Article"))

        assert response.status_code == status.HTTP_200_OK
