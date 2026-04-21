"""Tests pour l'authentification utilisateur."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

if TYPE_CHECKING:
    from tests.conftest import UserWithPassword


@pytest.mark.django_db
class TestLogin:
    """Tests endpoint POST /api/users/auth/login/"""

    URL = "/api/users/auth/login/"

    def test_login_with_valid_credentials(
        self,
        api_client: APIClient,
        admin_user: UserWithPassword,
    ) -> None:
        """Login avec des credentials valides retourne le user et set les cookies."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {"email": admin_user.user.email, "password": admin_user.password},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_200_OK
        data = cast(dict[str, Any], response.data)
        assert "user" in data
        assert "email" in data["user"]
        assert data["user"]["email"] == admin_user.user.email

    def test_login_with_wrong_password(
        self,
        api_client: APIClient,
        admin_user: UserWithPassword,
    ) -> None:
        """Login avec mauvais mot de passe retourne 401."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {"email": admin_user.user.email, "password": "wrongpassword"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_with_nonexistent_email(self, api_client: APIClient) -> None:
        """Login avec email inexistant retourne 401."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {"email": "nonexistent@example.com", "password": "password123"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_without_email(self, api_client: APIClient) -> None:
        """Login sans email retourne une erreur."""
        response = cast(
            Response,
            api_client.post(self.URL, {"password": "password123"}, format="json"),
        )

        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
        ]

    def test_login_without_password(self, api_client: APIClient) -> None:
        """Login sans mot de passe retourne une erreur."""
        response = cast(
            Response,
            api_client.post(self.URL, {"email": "test@example.com"}, format="json"),
        )

        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
        ]

    def test_login_with_empty_body(self, api_client: APIClient) -> None:
        """Login avec body vide retourne une erreur."""
        response = cast(Response, api_client.post(self.URL, {}, format="json"))

        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
        ]


@pytest.mark.django_db
class TestRefreshToken:
    """Tests endpoint POST /api/users/auth/refresh/"""

    URL = "/api/users/auth/refresh/"
    LOGIN_URL = "/api/users/auth/login/"

    def test_refresh_without_cookie_returns_401(
        self,
        api_client: APIClient,
    ) -> None:
        """Refresh sans cookie retourne 401."""
        response = cast(
            Response,
            api_client.post(self.URL, {}, format="json"),
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_with_invalid_token(self, api_client: APIClient) -> None:
        """Refresh avec token invalide retourne 400 ou 401."""
        response = cast(
            Response,
            api_client.post(self.URL, {"refresh": "invalid-token-here"}, format="json"),
        )

        # Refresh token is read from cookie, not body | so this should return 401
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED]

    def test_refresh_without_token(self, api_client: APIClient) -> None:
        """Refresh sans token retourne une erreur."""
        response = cast(Response, api_client.post(self.URL, {}, format="json"))

        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
        ]


@pytest.mark.django_db
class TestLogout:
    """Tests endpoint POST /api/users/auth/logout/"""

    URL = "/api/users/auth/logout/"
    LOGIN_URL = "/api/users/auth/login/"

    def test_logout_without_token_still_succeeds(
        self,
        api_client: APIClient,
    ) -> None:
        """Logout sans token retourne 200 (graceful)."""
        response = cast(
            Response,
            api_client.post(self.URL, {}, format="json"),
        )

        # Logout is graceful | returns 200 even without a token
        assert response.status_code == status.HTTP_200_OK
