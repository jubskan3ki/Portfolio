"""Service pour calculer les statistiques des experiences."""

from collections import Counter
from typing import Any

from django.db.models import Count

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

        all_technologies: list[str] = []
        for technologies in Experience.objects.exclude(
            technologies__isnull=True,
        ).values_list("technologies", flat=True):
            if technologies:
                all_technologies.extend(technologies)

        tech_counter = Counter(all_technologies)
        top_technologies = [{"name": tech, "level": count} for tech, count in tech_counter.most_common(10)]

        experience_by_type = ExperienceType.objects.annotate(count=Count("experiences")).values("name", "count", "icon")

        return {
            "totalYears": total_years,
            "companiesCount": companies_count,
            "topTechnologies": top_technologies,
            "experienceByType": [
                {"type": item["name"], "count": item["count"], "icon": item["icon"]} for item in experience_by_type
            ],
        }
