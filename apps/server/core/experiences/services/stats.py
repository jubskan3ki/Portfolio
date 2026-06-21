"""Service pour calculer les statistiques des experiences."""

from collections import Counter
from typing import Any

from django.db import connection
from django.db.models import Count, F, Func, TextField

from ..models import Experience, ExperienceType
from .timeline import TimelineService


class StatsService:
    """Service pour calculer les statistiques des experiences."""

    @staticmethod
    def get_stats() -> dict[str, Any]:
        """Calcule les statistiques globales des experiences.

        Returns:
            Dictionnaire des statistiques.
        """
        total_years = TimelineService.calculate_total_years()
        companies_count = Experience.objects.values("company").distinct().count()

        top_technologies = StatsService._get_top_technologies()

        experience_by_type = ExperienceType.objects.annotate(count=Count("experiences")).values("name", "count", "icon")

        return {
            "totalYears": total_years,
            "companiesCount": companies_count,
            "topTechnologies": top_technologies,
            "experienceByType": [
                {"type": item["name"], "count": item["count"], "icon": item["icon"]} for item in experience_by_type
            ],
        }

    @staticmethod
    def _get_top_technologies(limit: int = 10) -> list[dict[str, Any]]:
        """Top technologies par occurrence.

        Sur PostgreSQL, l'agregation est poussee en base via jsonb_array_elements_text
        (un GROUP BY/COUNT cote SQL, sans rapatrier toute la colonne JSON). Sur les
        autres backends (SQLite en tests), on retombe sur un comptage Python.
        """
        base = Experience.objects.exclude(technologies__isnull=True).exclude(technologies=[])

        if connection.vendor == "postgresql":
            rows = (
                base.annotate(
                    tech=Func(F("technologies"), function="jsonb_array_elements_text", output_field=TextField())
                )
                .values("tech")
                .annotate(level=Count("pk"))
                .order_by("-level", "tech")[:limit]
            )
            return [{"name": row["tech"], "level": row["level"]} for row in rows]

        all_technologies: list[str] = []
        for technologies in base.values_list("technologies", flat=True):
            if technologies:
                all_technologies.extend(technologies)

        tech_counter = Counter(all_technologies)
        return [{"name": tech, "level": count} for tech, count in tech_counter.most_common(limit)]
