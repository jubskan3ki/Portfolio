"""Configuration et fixtures pour les tests pytest."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

import pytest
from django.conf import settings
from django.core.cache import cache
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from utils.security.sessions import SessionManager

from .factories import (
    AdminFactory,
    ArticleCategoryFactory,
    ArticleFactory,
    ExperienceFactory,
    ExperienceTypeFactory,
    ProjectCategoryFactory,
    ProjectFactory,
    StackCategoryFactory,
    StackFactory,
    TagFactory,
    UserFactory,
)

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser


class UserWithPassword:
    """Wrapper pour un utilisateur avec son mot de passe."""

    def __init__(self, user: AbstractUser, password: str) -> None:
        self.user = user
        self.password = password


@pytest.fixture
def api_client() -> APIClient:
    """Retourne un client API non authentifie."""
    return APIClient()


@pytest.fixture
def admin_user(db: Any) -> UserWithPassword:
    """Cree et retourne un utilisateur admin avec son mot de passe."""
    del db
    password = "TestPassword123!"
    user = AdminFactory(password=password)
    return UserWithPassword(user, password)


@pytest.fixture
def regular_user(db: Any) -> UserWithPassword:
    """Cree et retourne un utilisateur regulier avec son mot de passe."""
    del db
    password = "TestPassword123!"
    user = UserFactory(password=password)
    return UserWithPassword(user, password)


def _issue_access_token_with_session(user: AbstractUser) -> str:
    """Emet un access token + enregistre la session (JWTCookieAuthentication l'exige)."""
    session_id = uuid.uuid4().hex
    refresh = RefreshToken.for_user(user)
    refresh["session_id"] = session_id
    refresh.access_token["session_id"] = session_id
    SessionManager(user.pk).add_session(
        session_id,
        {
            "browser": "test",
            "os": "test",
            "is_mobile": False,
            "ip_address": "127.0.0.1",
            "refresh_jti": str(refresh.get("jti", "")),
        },
    )
    return str(refresh.access_token)


@pytest.fixture
def admin_token(admin_user: UserWithPassword) -> str:
    """Retourne un token JWT pour l'admin (avec session enregistree)."""
    return _issue_access_token_with_session(admin_user.user)


@pytest.fixture
def user_token(regular_user: UserWithPassword) -> str:
    """Retourne un token JWT pour un utilisateur regulier (avec session enregistree)."""
    return _issue_access_token_with_session(regular_user.user)


@pytest.fixture
def authenticated_client(api_client: APIClient, admin_token: str) -> APIClient:
    """Retourne un client API authentifie en tant qu'admin (cookie HTTPOnly)."""
    api_client.cookies[settings.AUTH_COOKIE_ACCESS] = admin_token
    return api_client


@pytest.fixture
def user_client(api_client: APIClient, user_token: str) -> APIClient:
    """Retourne un client API authentifie en tant qu'utilisateur regulier (cookie HTTPOnly)."""
    api_client.cookies[settings.AUTH_COOKIE_ACCESS] = user_token
    return api_client


# Fixtures pour les donnees de test


@pytest.fixture
def sample_category(db: Any) -> dict[str, Any]:
    """Cree une categorie de test."""
    del db
    obj = ArticleCategoryFactory()
    return {
        "id": obj.id,
        "name": obj.name,
        "slug": obj.slug,
        "instance": obj,
    }


@pytest.fixture
def sample_tag(db: Any) -> dict[str, Any]:
    """Cree un tag de test."""
    del db
    obj = TagFactory()
    return {
        "id": obj.id,
        "name": obj.name,
        "instance": obj,
    }


@pytest.fixture
def sample_article(
    db: Any,
    sample_category: dict[str, Any],
) -> dict[str, Any]:
    """Cree un article de test."""
    del db
    obj = ArticleFactory(category=sample_category["instance"])
    return {
        "id": obj.id,
        "title": obj.title,
        "slug": obj.slug,
        "instance": obj,
    }


@pytest.fixture
def sample_experience_type(db: Any) -> dict[str, Any]:
    """Cree un type d'experience de test."""
    del db
    obj = ExperienceTypeFactory()
    return {
        "id": obj.id,
        "name": obj.name,
        "instance": obj,
    }


@pytest.fixture
def sample_experience(
    db: Any,
    sample_experience_type: dict[str, Any],
) -> dict[str, Any]:
    """Cree une experience de test."""
    del db
    obj = ExperienceFactory(type=sample_experience_type["instance"])
    return {
        "id": obj.id,
        "title": obj.title,
        "instance": obj,
    }


@pytest.fixture
def sample_project_category(db: Any) -> dict[str, Any]:
    """Cree une categorie de projet de test."""
    del db
    obj = ProjectCategoryFactory()
    return {
        "id": obj.id,
        "name": obj.name,
        "slug": obj.slug,
        "instance": obj,
    }


@pytest.fixture
def sample_project(
    db: Any,
    sample_project_category: dict[str, Any],
) -> dict[str, Any]:
    """Cree un projet de test."""
    del db
    obj = ProjectFactory(category=sample_project_category["instance"])
    return {
        "id": obj.id,
        "title": obj.title,
        "slug": obj.slug,
        "instance": obj,
    }


@pytest.fixture
def sample_stack_category(db: Any) -> dict[str, Any]:
    """Cree une categorie de stack de test."""
    del db
    obj = StackCategoryFactory()
    return {
        "id": obj.id,
        "name": obj.name,
        "instance": obj,
    }


@pytest.fixture
def sample_stack(
    db: Any,
    sample_stack_category: dict[str, Any],
) -> dict[str, Any]:
    """Cree un stack de test."""
    del db
    obj = StackFactory(category=sample_stack_category["instance"])
    return {
        "id": obj.id,
        "name": obj.name,
        "slug": obj.slug,
        "instance": obj,
    }


@pytest.fixture(autouse=True)
def _clear_cache():
    """Clear Django cache before each test to prevent throttle state leaking."""
    cache.clear()
