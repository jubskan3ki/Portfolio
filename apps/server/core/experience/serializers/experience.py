"""
Sérialisation des expériences professionnelles et éducatives.
"""

from datetime import datetime

from rest_framework import serializers

from ..models import Experience


class ExperienceSerializer(serializers.ModelSerializer):
    """
    Sérialiseur des expériences avec validations avancées.
    """

    class Meta:
        """
        Métadonnées du sérialiseur.
        """

        model = Experience
        fields = [
            "id",
            "title",
            "company_or_school",
            "location",
            "start_date",
            "end_date",
            "description",
            "experience_type",
            "logo",
            "created_at",
            "updated_at",
        ]

    def validate_end_date(self, value):
        """
        Valide que la end_date n'est pas antérieure à la start_date.
        Gère également le format de la date de début.
        """
        start_date_str = self.initial_data.get("start_date")

        if not start_date_str or not value:
            return value

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError as exc:
            raise serializers.ValidationError("Format invalide pour la date de début (YYYY-MM-DD attendu).") from exc

        if value < start_date:
            raise serializers.ValidationError("La date de fin ne peut pas être antérieure à la date de début.")

        return value

    def validate_logo(self, value):
        """
        Vérifie que le fichier logo ne dépasse pas la taille maximale autorisée.
        """
        max_size = 2 * 1024 * 1024

        if value and hasattr(value, "size"):
            if value.size > max_size:
                raise serializers.ValidationError("Le logo ne doit pas dépasser 2 Mo.")

        return value
