"""
Sérialisation des expériences professionnelles et éducatives.
"""

from datetime import datetime

from rest_framework import serializers

from ..models import Experience


class ExperienceSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les expériences professionnelles et éducatives.
    """

    duration = serializers.IntegerField(read_only=True)
    is_current = serializers.BooleanField(read_only=True)
    skills_acquired = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)

    class Meta:
        """
        Métadonnées du sérialiseur.
        """

        model = Experience
        fields = [
            "id",
            "title",
            "slug",
            "company_or_school",
            "location",
            "start_date",
            "end_date",
            "description",
            "skills_acquired",
            "experience_type",
            "is_highlighted",
            "website",
            "logo",
            "duration",
            "is_current",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "created_at", "updated_at"]

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
        Vérifie que le logo ne dépasse pas 2 Mo.
        """
        max_size = 2 * 1024 * 1024
        if value and hasattr(value, "size") and value.size > max_size:
            raise serializers.ValidationError("Le logo ne doit pas dépasser 2 Mo.")
        return value

    def validate_skills_acquired(self, value):
        """
        Vérifie que les compétences fournies sont sous forme de liste.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Les compétences doivent être fournies sous forme de liste.")
        return value
