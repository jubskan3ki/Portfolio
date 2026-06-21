"""Service pour les statistiques des stacks."""

import logging
from typing import Any, TypedDict

from django.db.models import Avg, Count, Max
from django.utils import timezone

from ..models import Stack, StackCategory

logger = logging.getLogger("core.stacks")


class CategoryCount(TypedDict):
    """Type pour le comptage par categorie."""

    category: str
    count: int


class StackLevel(TypedDict):
    """Type pour le niveau d'une stack."""

    name: str
    level: float


class StackExperience(TypedDict):
    """Type pour l'experience d'une stack."""

    name: str
    years: float


class StackStats(TypedDict):
    """Type pour les statistiques globales."""

    totalStacks: int
    totalCategories: int
    totalExperienceYears: float
    stacksByCategory: list[CategoryCount]
    averageProficiency: float
    topStacks: list[StackLevel]
    yearsOfExperience: list[StackExperience]


class StatsService:
    """Service pour les statistiques des stacks."""

    TOP_STACKS_LIMIT = 5
    EXPERIENCE_LIMIT = 10

    @staticmethod
    def get_stats() -> StackStats:
        """Calcule les statistiques globales des stacks.

        Returns:
            Dictionnaire avec toutes les statistiques.
        """
        aggregates = Stack.objects.aggregate(
            total=Count("id"),
            avg_level=Avg("level"),
        )

        total_stacks = aggregates["total"] or 0
        average_level = aggregates["avg_level"] or 0.0

        categories_data = (
            StackCategory.objects.annotate(count=Count("stacks")).values("name", "count").order_by("-count")
        )

        stacks_by_category: list[CategoryCount] = [
            {"category": item["name"], "count": item["count"]} for item in categories_data
        ]

        top_stacks_data = Stack.objects.order_by("-level").values("name", "level")[: StatsService.TOP_STACKS_LIMIT]

        top_stacks: list[StackLevel] = [
            {"name": item["name"], "level": float(item["level"])} for item in top_stacks_data
        ]

        today = timezone.now().date()

        def _months_since(started: Any) -> int:
            return max(0, (today.year - started.year) * 12 + (today.month - started.month))

        # Une seule requete : on derive a la fois la liste (limitee) et le total
        # (sur toutes les stacks datees) sans relancer de SELECT.
        dated_stacks = list(
            Stack.objects.filter(started_date__isnull=False).order_by("started_date").values("name", "started_date")
        )

        years_of_experience: list[StackExperience] = [
            {"name": item["name"], "years": round(_months_since(item["started_date"]) / 12, 1)}
            for item in dated_stacks[: StatsService.EXPERIENCE_LIMIT]
        ]

        total_experience_months = sum(_months_since(item["started_date"]) for item in dated_stacks)

        return {
            "totalStacks": total_stacks,
            "totalCategories": len(stacks_by_category),
            "totalExperienceYears": round(total_experience_months / 12, 1),
            "stacksByCategory": stacks_by_category,
            "averageProficiency": round(average_level, 1),
            "topStacks": top_stacks,
            "yearsOfExperience": years_of_experience,
        }

    @staticmethod
    def get_summary() -> dict[str, Any]:
        """Retourne un resume rapide des statistiques."""
        return Stack.objects.aggregate(
            total=Count("id"),
            avg_level=Avg("level"),
            max_level=Max("level"),
        )
