"""
Sérialisation des expériences professionnelles et éducatives.
"""

from datetime import datetime

from rest_framework import serializers

from .models import Experience


class ExperienceSerializer(serializers.ModelSerializer):
    """
    Sérialisation des expériences.
    """

    class Meta:
        model = Experience
        fields = "__all__"

    def validate_end_date(self, value):
        """
        Validation de la cohérence des dates (end_date ne peut pas être avant start_date).
        """
        start_date_str = self.initial_data.get("start_date")
        if start_date_str and value:
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            except ValueError as exc:
                raise serializers.ValidationError("Format de date invalide pour start_date.") from exc

            if value < start_date:
                raise serializers.ValidationError("La date de fin ne peut pas être antérieure à la date de début.")
        return value
