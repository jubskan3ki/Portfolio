"""Helpers pour l'extraction et la validation des filtres API."""

from typing import TypedDict

from django.db.models import Model, QuerySet
from rest_framework.request import Request

from config.constants import (
    QUERY_PARAM_CATEGORY,
    QUERY_PARAM_LIMIT,
    QUERY_PARAM_PAGE,
    QUERY_PARAM_SEARCH,
    QUERY_PARAM_SORT_BY,
    QUERY_PARAM_SORT_DIRECTION,
    QUERY_PARAM_TAG,
)

from .helpers import parse_bool, parse_limit, parse_page, parse_sort_direction


class BaseFilters(TypedDict, total=False):
    """Structure de base pour les filtres communs."""

    search: str | None
    category: str | None
    sort_by: str | None
    sort_direction: str
    limit: int
    page: int


class ArticleFilters(BaseFilters, total=False):
    """Filtres specifiques aux articles."""

    tag: str | None
    is_featured: bool | None
    is_published: bool | None


class ProjectFilters(BaseFilters, total=False):
    """Filtres specifiques aux projets."""

    status: str | None
    is_featured: bool | None
    technologies: list[str]


class StackFilters(BaseFilters, total=False):
    """Filtres specifiques aux stacks."""

    level_min: int | None
    level_max: int | None
    min_level: float | None
    min_experience: int | None
    tags: list[str]
    is_featured: bool | None


class ExperienceFilters(BaseFilters, total=False):
    """Filtres specifiques aux experiences."""

    type: str | None
    start_year: int | None
    end_year: int | None
    technologies: list[str]


def extract_base_filters(request: Request) -> BaseFilters:
    """Extrait les filtres communs depuis la requete.

    Args:
        request: Requete DRF

    Returns:
        Dictionnaire des filtres de base
    """
    params = request.query_params

    return BaseFilters(
        search=params.get(QUERY_PARAM_SEARCH) or None,
        category=params.get(QUERY_PARAM_CATEGORY) or None,
        sort_by=params.get(QUERY_PARAM_SORT_BY) or None,
        sort_direction=parse_sort_direction(params.get(QUERY_PARAM_SORT_DIRECTION)),
        limit=parse_limit(params.get(QUERY_PARAM_LIMIT)),
        page=parse_page(params.get(QUERY_PARAM_PAGE)),
    )


def extract_article_filters(request: Request) -> ArticleFilters:
    """Extrait les filtres pour les articles.

    Args:
        request: Requete DRF

    Returns:
        Dictionnaire des filtres articles
    """
    base = extract_base_filters(request)
    params = request.query_params

    return ArticleFilters(
        **base,
        tag=params.get(QUERY_PARAM_TAG) or None,
        is_featured=parse_bool(params.get("isFeatured")) if "isFeatured" in params else None,
        is_published=parse_bool(params.get("isPublished")) if "isPublished" in params else None,
    )


def extract_project_filters(request: Request) -> ProjectFilters:
    """Extrait les filtres pour les projets.

    Args:
        request: Requete DRF

    Returns:
        Dictionnaire des filtres projets
    """
    base = extract_base_filters(request)
    params = request.query_params

    return ProjectFilters(
        **base,
        status=params.get("status") or None,
        is_featured=parse_bool(params.get("isFeatured")) if "isFeatured" in params else None,
    )


def extract_stack_filters(request: Request) -> StackFilters:
    """Extrait les filtres pour les stacks.

    Args:
        request: Requete DRF

    Returns:
        Dictionnaire des filtres stacks
    """
    base = extract_base_filters(request)
    params = request.query_params

    level_min = params.get("levelMin")
    level_max = params.get("levelMax")

    return StackFilters(
        **base,
        level_min=int(level_min) if level_min and level_min.isdigit() else None,
        level_max=int(level_max) if level_max and level_max.isdigit() else None,
        is_featured=parse_bool(params.get("isFeatured")) if "isFeatured" in params else None,
    )


def extract_experience_filters(request: Request) -> ExperienceFilters:
    """Extrait les filtres pour les experiences.

    Args:
        request: Requete DRF

    Returns:
        Dictionnaire des filtres experiences
    """
    base = extract_base_filters(request)
    params = request.query_params

    start_year = params.get("startYear")
    end_year = params.get("endYear")

    return ExperienceFilters(
        **base,
        type=params.get("type") or None,
        start_year=int(start_year) if start_year and start_year.isdigit() else None,
        end_year=int(end_year) if end_year and end_year.isdigit() else None,
    )


def apply_sorting[M: Model](
    queryset: QuerySet[M],
    sort_by: str | None,
    sort_direction: str,
    field_mapping: dict[str, str],
    default_field: str = "-created_at",
) -> QuerySet[M]:
    """Applique le tri sur un queryset.

    Args:
        queryset: QuerySet Django
        sort_by: Champ de tri demande (cle du mapping)
        sort_direction: 'asc' ou 'desc'
        field_mapping: Mapping nom API -> nom champ DB
        default_field: Champ de tri par defaut

    Returns:
        QuerySet trie
    """
    if not sort_by or sort_by not in field_mapping:
        return queryset.order_by(default_field)

    db_field = field_mapping[sort_by]
    prefix = "" if sort_direction == "asc" else "-"
    return queryset.order_by(f"{prefix}{db_field}")
