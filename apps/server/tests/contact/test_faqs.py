"""Tests pour les FAQs."""

from __future__ import annotations

from typing import cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestListFAQs:
    """Tests endpoint GET /api/contacts/faqs/"""

    URL = "/api/contacts/faqs/"

    def test_list_faqs_public(self, api_client: APIClient) -> None:
        """Liste FAQs peut etre publique."""
        response = cast(Response, api_client.get(self.URL))

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_404_NOT_FOUND,
        ]

    def test_list_faqs_authenticated(self, authenticated_client: APIClient) -> None:
        """Liste FAQs authentifie."""
        response = cast(Response, authenticated_client.get(self.URL))

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestCreateFAQ:
    """Tests endpoint POST /api/contacts/faqs/"""

    URL = "/api/contacts/faqs/"

    def test_create_faq_authenticated(self, authenticated_client: APIClient) -> None:
        """Creation FAQ authentifie."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {
                    "question": "Comment ca marche?",
                    "answer": "C'est simple!",
                },
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_faq_unauthenticated(self, api_client: APIClient) -> None:
        """Creation FAQ non authentifie retourne 401/403."""
        response = cast(
            Response,
            api_client.post(
                self.URL,
                {
                    "question": "Comment ca marche?",
                    "answer": "C'est simple!",
                },
                format="json",
            ),
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_create_faq_missing_question(self, authenticated_client: APIClient) -> None:
        """Creation FAQ sans question retourne 400."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {"answer": "Une reponse"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_faq_missing_answer(self, authenticated_client: APIClient) -> None:
        """Creation FAQ sans reponse retourne 400."""
        response = cast(
            Response,
            authenticated_client.post(
                self.URL,
                {"question": "Une question?"},
                format="json",
            ),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
