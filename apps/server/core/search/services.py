"""Service orchestrant la recherche full-text sur Articles, Projects, Stacks, Experiences."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
)
from django.db import connection
from django.db.models import F, Q, QuerySet

from core.articles.models import Article
from core.experiences.models import Experience
from core.projects.models import Project
from core.stacks.models import Stack
from utils.filters import build_prefix_tsquery

SEARCH_CONFIG_NAME = "french_unaccent"

HEADLINE_OPTIONS = "StartSel=<mark>, StopSel=</mark>, MaxFragments=2, MaxWords=20, MinWords=5"

VALID_TYPES: tuple[str, ...] = ("all", "articles", "projects", "stacks", "experiences")
SEARCHABLE_TYPES: tuple[str, ...] = ("articles", "projects", "stacks", "experiences")

MIN_QUERY_LENGTH = 2


@dataclass(frozen=True)
class SearchResult:
    """Resultat unitaire de recherche, prêt pour serialisation."""

    type: str
    id: int
    slug: str
    title: str
    url: str
    rank: float
    snippet: str
    metadata: dict[str, Any]


class SearchService:
    """Orchestre une recherche multi-entite avec ranking et highlighting."""

    CONFIGS: ClassVar[dict[str, dict[str, Any]]] = {
        "articles": {
            "model": Article,
            "title_field": "title",
            "slug_field": "slug",
            "headline_field": "excerpt",
            "fallback_fields": ("title", "excerpt"),
            "url_template": "/blog/{slug}",
        },
        "projects": {
            "model": Project,
            "title_field": "title",
            "slug_field": "slug",
            "headline_field": "description",
            "fallback_fields": ("title", "description", "long_description"),
            "url_template": "/projects/{slug}",
        },
        "stacks": {
            "model": Stack,
            "title_field": "name",
            "slug_field": "slug",
            "headline_field": "description",
            "fallback_fields": ("name", "description", "content"),
            "url_template": "/stacks/{slug}",
        },
        "experiences": {
            "model": Experience,
            "title_field": "title",
            "slug_field": None,
            "headline_field": "description",
            "fallback_fields": ("title", "company", "description"),
            "url_template": "/experiences/{id}",
        },
    }

    def __init__(self, query: str, types: list[str], user: Any = None) -> None:
        self.query = query.strip()
        self.types = self._normalize_types(types)
        self.user = user

    @staticmethod
    def _normalize_types(types: list[str]) -> list[str]:
        if not types or "all" in types:
            return list(SEARCHABLE_TYPES)
        return [t for t in types if t in SEARCHABLE_TYPES]

    @classmethod
    def is_postgres(cls) -> bool:
        return connection.vendor == "postgresql"

    def run(self) -> list[SearchResult]:
        """Execute la recherche sur tous les types demandes, tries par rank desc."""
        if len(self.query) < MIN_QUERY_LENGTH:
            return []

        results: list[SearchResult] = []
        for type_name in self.types:
            results.extend(self._search_type(type_name))

        results.sort(key=lambda r: r.rank, reverse=True)
        return results

    def _search_type(self, type_name: str) -> list[SearchResult]:
        config = self.CONFIGS[type_name]
        queryset = self._get_base_queryset(type_name, config["model"])

        if self.is_postgres():
            return self._search_postgres(type_name, config, queryset)
        return self._search_fallback(type_name, config, queryset)

    def _get_base_queryset(self, type_name: str, model: type) -> QuerySet:
        queryset = model.objects.all()
        if type_name == "articles" and not (self.user and getattr(self.user, "is_staff", False)):
            queryset = queryset.filter(is_published=True)
        return queryset

    def _search_postgres(
        self,
        type_name: str,
        config: dict[str, Any],
        queryset: QuerySet,
    ) -> list[SearchResult]:
        # Prefix-enabled tsquery (ex: "nux" -> "nux:*") pour que les saisies partielles
        # matchent. Sans ca, `SearchQuery(..., search_type="websearch")` ne matche
        # que les mots complets stemmes, donc `nux` ne trouve jamais Nuxt.
        raw_tsquery = build_prefix_tsquery(self.query)
        if not raw_tsquery:
            return []
        search_query = SearchQuery(raw_tsquery, config=SEARCH_CONFIG_NAME, search_type="raw")
        # SearchHeadline a besoin d'une tsquery qui match le texte en clair | on en
        # construit une seconde version `plain` pour conserver le highlighting propre.
        headline_query = SearchQuery(self.query, config=SEARCH_CONFIG_NAME, search_type="plain")
        headline_field = config["headline_field"]

        # IMPORTANT: pass F("search_vector") (not the string) so Django does NOT
        # wrap it with to_tsvector(col::text), which would strip the stored A/B/C weights.
        annotated = (
            queryset.annotate(
                rank=SearchRank(F("search_vector"), search_query),
                snippet=SearchHeadline(
                    headline_field,
                    headline_query,
                    config=SEARCH_CONFIG_NAME,
                    start_sel="<mark>",
                    stop_sel="</mark>",
                    max_fragments=2,
                    max_words=20,
                    min_words=5,
                ),
            )
            .filter(search_vector=search_query)
            .order_by("-rank")
        )

        return [self._build_result(type_name, config, obj, rank=obj.rank, snippet=obj.snippet) for obj in annotated]

    def _search_fallback(
        self,
        type_name: str,
        config: dict[str, Any],
        queryset: QuerySet,
    ) -> list[SearchResult]:
        """Fallback icontains pour SQLite (tests) et autres backends non-PG."""
        q = Q()
        for field in config["fallback_fields"]:
            q |= Q(**{f"{field}__icontains": self.query})
        matched = queryset.filter(q)

        return [
            self._build_result(
                type_name,
                config,
                obj,
                rank=0.0,
                snippet=self._fallback_snippet(obj, config["headline_field"]),
            )
            for obj in matched
        ]

    def _fallback_snippet(self, obj: Any, field: str) -> str:
        text = getattr(obj, field, "") or ""
        if not self.query:
            return text[:200]
        needle = self.query.lower()
        text_lc = text.lower()
        idx = text_lc.find(needle)
        if idx == -1:
            return text[:200]
        start = max(0, idx - 30)
        end = min(len(text), idx + len(self.query) + 30)
        snippet = text[start:end]
        highlighted = self._highlight_fallback(snippet, self.query)
        prefix = "..." if start > 0 else ""
        suffix = "..." if end < len(text) else ""
        return f"{prefix}{highlighted}{suffix}"

    @staticmethod
    def _highlight_fallback(text: str, query: str) -> str:
        from django.utils.html import escape

        escaped_text = escape(text)
        escaped_query = escape(query)
        lower = escaped_text.lower()
        needle = escaped_query.lower()
        idx = lower.find(needle)
        if idx == -1:
            return escaped_text
        return (
            escaped_text[:idx]
            + "<mark>"
            + escaped_text[idx : idx + len(escaped_query)]
            + "</mark>"
            + escaped_text[idx + len(escaped_query) :]
        )

    def _build_result(
        self,
        type_name: str,
        config: dict[str, Any],
        obj: Any,
        rank: float,
        snippet: str,
    ) -> SearchResult:
        title = getattr(obj, config["title_field"])
        slug_field = config["slug_field"]
        slug = getattr(obj, slug_field) if slug_field else ""
        url = config["url_template"].format(slug=slug, id=obj.id)
        return SearchResult(
            type=type_name.rstrip("s"),
            id=obj.id,
            slug=slug,
            title=str(title),
            url=url,
            rank=float(rank or 0.0),
            snippet=str(snippet or ""),
            metadata=self._build_metadata(type_name, obj),
        )

    @staticmethod
    def _build_metadata(type_name: str, obj: Any) -> dict[str, Any]:
        if type_name == "articles":
            return {
                "category": obj.category.name if obj.category_id else None,
                "published_date": obj.published_date.isoformat() if obj.published_date else None,
                "is_featured": obj.is_featured,
            }
        if type_name == "projects":
            return {
                "category": obj.category.name if obj.category_id else None,
                "technologies": obj.technologies or [],
                "date": obj.date.isoformat() if obj.date else None,
            }
        if type_name == "stacks":
            return {
                "category": obj.category.name if obj.category_id else None,
                "level": float(obj.level) if obj.level is not None else None,
            }
        if type_name == "experiences":
            return {
                "company": obj.company,
                "type": obj.type.name if obj.type_id else None,
                "start_date": obj.start_date.isoformat() if obj.start_date else None,
                "end_date": obj.end_date.isoformat() if obj.end_date else None,
            }
        return {}
