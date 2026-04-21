"""Tests pour le profil utilisateur."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

if TYPE_CHECKING:
    from tests.conftest import UserWithPassword


@pytest.mark.django_db
class TestGetProfile:
    """Tests endpoint GET /api/users/profile/"""

    URL = "/api/users/profile/"

    def test_get_profile_authenticated(
        self,
        authenticated_client: APIClient,
        admin_user: UserWithPassword,
    ) -> None:
        """Lecture profil authentifie retourne les donnees utilisateur."""
        response = cast(Response, authenticated_client.get(self.URL))

        assert response.status_code == status.HTTP_200_OK
        data = cast(dict[str, Any], response.data)
        assert data["email"] == admin_user.user.email
        assert "id" in data
        assert "first_name" in data
        assert "last_name" in data

    def test_get_profile_unauthenticated(self, api_client: APIClient) -> None:
        """Lecture profil non authentifie retourne 401."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUpdateProfile:
    """Tests endpoint PUT/PATCH /api/users/profile/"""

    URL = "/api/users/profile/"

    def test_update_profile_first_name(self, authenticated_client: APIClient) -> None:
        """Mise a jour du prenom reussit."""
        response = cast(
            Response,
            authenticated_client.put(self.URL, {"first_name": "Updated"}, format="json"),
        )

        assert response.status_code == status.HTTP_200_OK
        data = cast(dict[str, Any], response.data)
        assert data["first_name"] == "Updated"

    def test_update_profile_last_name(self, authenticated_client: APIClient) -> None:
        """Mise a jour du nom reussit."""
        response = cast(
            Response,
            authenticated_client.put(self.URL, {"last_name": "Name"}, format="json"),
        )

        assert response.status_code == status.HTTP_200_OK
        data = cast(dict[str, Any], response.data)
        assert data["last_name"] == "Name"

    def test_update_profile_bio(self, authenticated_client: APIClient) -> None:
        """Mise a jour de la bio reussit."""
        response = cast(
            Response,
            authenticated_client.put(self.URL, {"bio": "This is my bio"}, format="json"),
        )

        assert response.status_code == status.HTTP_200_OK
        data = cast(dict[str, Any], response.data)
        assert data["bio"] == "This is my bio"

    def test_update_profile_unauthenticated(self, api_client: APIClient) -> None:
        """Mise a jour profil non authentifie retourne 401."""
        response = cast(
            Response,
            api_client.put(self.URL, {"first_name": "Test"}, format="json"),
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile_social_urls(self, authenticated_client: APIClient) -> None:
        """PUT linkedin + github URLs n'est pas flag comme suspicious par le middleware security."""
        payload = {
            "linkedin": "https://www.linkedin.com/in/juba-aitadda/",
            "github": "https://github.com/jubskan3ki",
        }
        response = cast(
            Response,
            authenticated_client.put(self.URL, payload, format="json"),
        )

        assert response.status_code == status.HTTP_200_OK
        data = cast(dict[str, Any], response.data)
        assert data["linkedin"] == payload["linkedin"]
        assert data["github"] == payload["github"]


@pytest.mark.django_db
class TestPasswordReset:
    """Tests endpoints de reset mot de passe."""

    REQUEST_URL = "/api/users/request-reset-password/"
    RESET_URL = "/api/users/reset-password/"

    def test_request_reset_valid_email(
        self,
        api_client: APIClient,
        admin_user: UserWithPassword,
    ) -> None:
        """Demande reset avec email valide retourne succes."""
        response = cast(
            Response,
            api_client.post(self.REQUEST_URL, {"email": admin_user.user.email}, format="json"),
        )

        assert response.status_code == status.HTTP_200_OK

    def test_request_reset_nonexistent_email(self, api_client: APIClient) -> None:
        """Demande reset avec email inexistant retourne aussi succes (securite)."""
        response = cast(
            Response,
            api_client.post(self.REQUEST_URL, {"email": "nonexistent@example.com"}, format="json"),
        )

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
        ]

    def test_request_reset_invalid_email_format(self, api_client: APIClient) -> None:
        """Demande reset avec email invalide retourne 400 ou 200 (securite)."""
        response = cast(
            Response,
            api_client.post(self.REQUEST_URL, {"email": "not-an-email"}, format="json"),
        )

        # API may return 200 for security (not revealing if email validation failed)
        # or 400 for invalid format
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

    def test_reset_password_invalid_code(self, api_client: APIClient) -> None:
        """Reset avec code invalide retourne erreur."""
        response = cast(
            Response,
            api_client.post(
                self.RESET_URL,
                {
                    "email": "test@example.com",
                    "code": "INVALID",
                    "password": "NewPassword123!",
                    "confirm_password": "NewPassword123!",
                },
                format="json",
            ),
        )

        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_reset_password_mismatched_passwords(self, api_client: APIClient) -> None:
        """Reset avec mots de passe differents retourne 400."""
        response = cast(
            Response,
            api_client.post(
                self.RESET_URL,
                {
                    "email": "test@example.com",
                    "code": "12345678",
                    "password": "NewPassword123!",
                    "confirm_password": "DifferentPassword123!",
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
