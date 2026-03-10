"""Service pour les statistiques de contact."""

from typing import Any

from django.db.models import Avg, Count, DurationField, ExpressionWrapper, F

from ..models import Contact


class ContactStatsService:
    """Service pour les statistiques des contacts."""

    @staticmethod
    def get_stats() -> dict[str, Any]:
        """Calcule les statistiques globales des contacts."""
        total_messages = Contact.objects.count()

        if total_messages == 0:
            return {
                "totalMessages": 0,
                "responseRate": 0.0,
                "averageResponseTime": "0 heures",
                "popularSubjects": [],
            }

        responded_count = Contact.objects.filter(status__in=["responded", "closed"]).count()
        response_rate = (responded_count / total_messages) * 100

        average_response_time = ContactStatsService._calculate_avg_response_time()
        popular_subjects = ContactStatsService._get_popular_subjects()

        return {
            "totalMessages": total_messages,
            "responseRate": round(response_rate, 1),
            "averageResponseTime": average_response_time,
            "popularSubjects": popular_subjects,
        }

    @staticmethod
    def _calculate_avg_response_time() -> str:
        """Calcule le temps de reponse moyen via aggregation SQL."""
        result = Contact.objects.filter(
            status="responded",
            response_date__isnull=False,
        ).aggregate(
            avg_duration=Avg(
                ExpressionWrapper(
                    F("response_date") - F("created_at"),
                    output_field=DurationField(),
                )
            )
        )

        avg_duration = result["avg_duration"]
        if not avg_duration:
            return "0 heures"

        total_hours = avg_duration.total_seconds() / 3600
        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)
        return f"{hours} heures {minutes} minutes"

    @staticmethod
    def _get_popular_subjects() -> list[dict[str, Any]]:
        """Recupere les sujets les plus populaires."""
        subjects = Contact.objects.values("subject").annotate(count=Count("subject")).order_by("-count")[:5]
        return [{"subject": item["subject"], "count": item["count"]} for item in subjects]
