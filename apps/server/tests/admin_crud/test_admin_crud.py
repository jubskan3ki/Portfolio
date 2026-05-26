"""Tests POST/PATCH admin pour les 4 entites (projects, articles, stacks, experiences).

Valide les fixes : URLDictField parse JSON string, Experience snake_case,
RelativeMedia*Field renvoie des URLs relatives.

pytest -k admin_crud -n auto  -> execution parallele (avec pytest-xdist).
"""

from __future__ import annotations

import io
import json
from typing import Any, cast

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from tests.factories import (
    ExperienceTypeFactory,
    ProjectCategoryFactory,
    StackCategoryFactory,
)


def make_image_file(name: str = "test.png", color: str = "red") -> SimpleUploadedFile:
    """Genere un PNG en memoire (utilise les vrais bytes PIL pour ImageField)."""
    img = Image.new("RGB", (10, 10), color=color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return SimpleUploadedFile(name, buf.read(), content_type="image/png")


@pytest.mark.django_db
class TestProjectCreate:
    """POST /api/projects/ via multipart (forme exacte envoyee par l'admin Nuxt)."""

    URL = "/api/projects/"

    def test_create_project_with_links_json_string(
        self,
        authenticated_client: APIClient,
    ) -> None:
        """Regression : URLDictField doit parser un JSON string envoye via multipart."""
        category = ProjectCategoryFactory()

        payload = {
            "title": "Mon nouveau projet",
            "slug": "mon-nouveau-projet",
            "description": "Description courte",
            "category": str(category.id),
            "seo_title": "",
            "meta_description": "",
            "longDescription": "Description longue",
            "links": json.dumps({"demo": "https://demo.example.com", "github": "https://github.com/x/y"}),
            "technologies": json.dumps(["Vue", "Django"]),
        }

        response = cast(Response, authenticated_client.post(self.URL, data=payload, format="multipart"))

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_create_project_with_image_returns_relative_url(
        self,
        authenticated_client: APIClient,
    ) -> None:
        """Regression : l'URL d'image renvoyee doit etre relative (pas http://backend:8000/...)."""
        category = ProjectCategoryFactory()
        image = make_image_file("projet.png")

        payload = {
            "title": "Projet avec image",
            "slug": "projet-avec-image",
            "description": "Une desc",
            "category": str(category.id),
            "image": image,
        }

        response = cast(Response, authenticated_client.post(self.URL, data=payload, format="multipart"))

        assert response.status_code == status.HTTP_201_CREATED, response.data
        data = cast(dict[str, Any], response.data)
        img = data.get("image")
        assert img, "image manquante dans la response"
        assert img.startswith("/media/"), f"URL non relative: {img!r}"
        assert "backend" not in img, f"hostname interne leak: {img!r}"

    def test_create_project_without_links(
        self,
        authenticated_client: APIClient,
    ) -> None:
        """Sanity : creation sans links fonctionne."""
        category = ProjectCategoryFactory()

        payload = {
            "title": "Sans liens",
            "slug": "sans-liens",
            "description": "Desc",
            "category": str(category.id),
        }

        response = cast(Response, authenticated_client.post(self.URL, data=payload, format="multipart"))

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_create_project_unauthenticated(self, api_client: APIClient) -> None:
        """Sans auth on rejette."""
        category = ProjectCategoryFactory()
        payload = {
            "title": "Anon",
            "description": "x",
            "category": str(category.id),
        }
        response = cast(Response, api_client.post(self.URL, data=payload, format="multipart"))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


@pytest.mark.django_db
class TestArticleCreate:
    """POST /api/articles/ via multipart."""

    URL = "/api/articles/"

    def test_create_article_with_content_json_string(
        self,
        authenticated_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """Le content JSONBlockListField doit accepter un string JSON depuis multipart."""
        content_blocks = [{"type": "paragraph", "content": "Un paragraphe"}]

        payload = {
            "title": "Mon article",
            "slug": "mon-article",
            "excerpt": "Un excerpt",
            "content": json.dumps(content_blocks),
            "category": str(sample_category["id"]),
            "is_published": "true",
            "seo_title": "",
            "meta_description": "",
        }

        response = cast(Response, authenticated_client.post(self.URL, data=payload, format="multipart"))

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_create_article_with_image(
        self,
        authenticated_client: APIClient,
        sample_category: dict[str, Any],
    ) -> None:
        """L'image envoyee doit etre persistee et retournee en URL relative."""
        payload = {
            "title": "Article avec image",
            "slug": "article-avec-image",
            "excerpt": "x",
            "content": json.dumps([{"type": "paragraph", "content": "x"}]),
            "category": str(sample_category["id"]),
            "is_published": "false",
            "image": make_image_file("article.png"),
        }

        response = cast(Response, authenticated_client.post(self.URL, data=payload, format="multipart"))

        assert response.status_code == status.HTTP_201_CREATED, response.data
        data = cast(dict[str, Any], response.data)
        img = data.get("image")
        assert img and img.startswith("/media/"), f"URL non relative: {img!r}"


@pytest.mark.django_db
class TestStackCreate:
    """POST /api/stacks/ via multipart."""

    URL = "/api/stacks/"

    def test_create_stack_minimal(
        self,
        authenticated_client: APIClient,
    ) -> None:
        category = StackCategoryFactory()
        payload = {
            "name": "Vue.js",
            "category": str(category.id),
            "level": "4.5",
            "seo_title": "",
            "meta_description": "",
            "description": "Framework reactif",
        }

        response = cast(Response, authenticated_client.post(self.URL, data=payload, format="multipart"))

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_create_stack_with_logo(
        self,
        authenticated_client: APIClient,
    ) -> None:
        """Logo file renvoie URL relative."""
        category = StackCategoryFactory()
        payload = {
            "name": "Django",
            "category": str(category.id),
            "level": "5.0",
            "description": "Framework Python",
            "logo": make_image_file("django.png", color="green"),
        }

        response = cast(Response, authenticated_client.post(self.URL, data=payload, format="multipart"))

        assert response.status_code == status.HTTP_201_CREATED, response.data
        data = cast(dict[str, Any], response.data)
        if data.get("logo"):
            assert data["logo"].startswith("/media/"), f"URL non relative: {data['logo']!r}"


@pytest.mark.django_db
class TestExperienceCreate:
    """POST /api/experiences/ via multipart.

    Regression : ExperienceForm envoie start_date / end_date snake_case.
    """

    URL = "/api/experiences/"

    def test_create_experience_snake_case_dates(
        self,
        authenticated_client: APIClient,
    ) -> None:
        """Le serializer doit accepter start_date / end_date snake_case."""
        exp_type = ExperienceTypeFactory()
        payload = {
            "type": str(exp_type.id),
            "title": "Developpeur Full Stack",
            "company": "Anthropic",
            "location": "Paris",
            "start_date": "2024-01-15",
            "end_date": "2025-06-30",
            "description": "Mission backend Django + frontend Vue.",
        }

        response = cast(Response, authenticated_client.post(self.URL, data=payload, format="multipart"))

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_create_experience_camel_case_dates_still_works(
        self,
        authenticated_client: APIClient,
    ) -> None:
        """Backward compat : startDate / endDate camelCase reste accepte."""
        exp_type = ExperienceTypeFactory()
        payload = {
            "type": str(exp_type.id),
            "title": "Stage",
            "company": "X",
            "location": "Y",
            "startDate": "2024-01-01",
            "description": "Stage de fin d'etudes.",
        }

        response = cast(Response, authenticated_client.post(self.URL, data=payload, format="multipart"))

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_create_experience_missing_start_date_fails(
        self,
        authenticated_client: APIClient,
    ) -> None:
        """Si ni start_date ni startDate, on rejette avec un message utile."""
        exp_type = ExperienceTypeFactory()
        payload = {
            "type": str(exp_type.id),
            "title": "X",
            "company": "X",
            "location": "X",
            "description": "x",
        }

        response = cast(Response, authenticated_client.post(self.URL, data=payload, format="multipart"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_experience_future_start_date_fails(
        self,
        authenticated_client: APIClient,
    ) -> None:
        """Date dans le futur rejetee."""
        exp_type = ExperienceTypeFactory()
        payload = {
            "type": str(exp_type.id),
            "title": "X",
            "company": "X",
            "location": "X",
            "start_date": "2099-01-01",
            "description": "x",
        }

        response = cast(Response, authenticated_client.post(self.URL, data=payload, format="multipart"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_experience_with_logo(
        self,
        authenticated_client: APIClient,
    ) -> None:
        """Logo file renvoie URL relative."""
        exp_type = ExperienceTypeFactory()
        payload = {
            "type": str(exp_type.id),
            "title": "Mission",
            "company": "ACME",
            "location": "Remote",
            "start_date": "2023-01-01",
            "description": "Mission",
            "logo": make_image_file("logo.png", color="blue"),
        }

        response = cast(Response, authenticated_client.post(self.URL, data=payload, format="multipart"))

        assert response.status_code == status.HTTP_201_CREATED, response.data
        data = cast(dict[str, Any], response.data)
        if data.get("logo"):
            assert data["logo"].startswith("/media/"), f"URL non relative: {data['logo']!r}"
