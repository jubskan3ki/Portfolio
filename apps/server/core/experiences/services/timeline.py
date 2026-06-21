"""Service pour generer des visualisations de type timeline des experiences."""

from datetime import date
from typing import Any

from django.utils.timezone import now

from ..models import Experience


class TimelineService:
    """Service pour generer des visualisations des experiences."""

    @staticmethod
    def get_timeline() -> list[dict[str, Any]]:
        """Recupere les experiences groupees par annee pour affichage en timeline.

        Returns:
            Liste d'objets {year, experiences} tries par annee decroissante.
        """
        experiences = Experience.objects.select_related("type").order_by("-start_date")

        timeline: dict[int | None, list[Experience]] = {}
        for exp in experiences:
            year = exp.year
            if year not in timeline:
                timeline[year] = []
            timeline[year].append(exp)

        sorted_items = sorted(timeline.items(), key=lambda x: x[0] or 0, reverse=True)
        return [{"year": year, "experiences": exps} for year, exps in sorted_items]

    @staticmethod
    def calculate_total_years() -> float:
        """Calcule le nombre total d'annees d'experience (sans chevauchement).

        Returns:
            Nombre total d'annees d'experience.
        """
        experiences = list(Experience.objects.order_by("start_date"))

        if not experiences:
            return 0.0

        today = now().date()
        total_months = 0
        current_period_end: date | None = None

        for exp in experiences:
            start = exp.start_date
            end = exp.end_date or today

            if current_period_end is None or start > current_period_end:
                total_months += exp.duration_months
                current_period_end = end
            elif end > current_period_end:
                years_diff = end.year - current_period_end.year
                months_diff = end.month - current_period_end.month
                total_months += years_diff * 12 + months_diff
                current_period_end = end

        return round(total_months / 12, 1)

    @staticmethod
    def get_current() -> Experience | None:
        """Recupere l'experience en cours (sans date de fin).

        Delegue a ExperienceService pour eviter la duplication.

        Returns:
            L'experience en cours ou None.
        """
        from .experience import ExperienceService

        return ExperienceService.get_current()
