"""Serializers pour les experiences professionnelles."""

from django.utils import timezone
from rest_framework import serializers

from utils.serializers import ReadOnlySerializer

from ..models import Experience, ExperienceType


class ExperienceWriteSerializer(serializers.ModelSerializer):
    """Serializer pour la creation et mise a jour des experiences."""

    type = serializers.PrimaryKeyRelatedField(queryset=ExperienceType.objects.all())
    # Accept camelCase from frontend, map to model snake_case fields
    startDate = serializers.DateField(source="start_date", required=True)
    endDate = serializers.DateField(source="end_date", required=False, allow_null=True)

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "company",
            "location",
            "startDate",
            "endDate",
            "description",
            "logo",
            "technologies",
            "achievements",
            "type",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "technologies": {"required": False},
            "achievements": {"required": False},
            "logo": {"required": False},
        }

    def validate(self, attrs):
        """Validate dates: start_date not in future, end_date after start_date."""
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and start_date > timezone.now().date():
            raise serializers.ValidationError({"startDate": "La date de debut ne peut pas etre dans le futur."})

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError({"endDate": "La date de fin doit etre posterieure a la date de debut."})

        return attrs


class ExperienceSerializer(serializers.ModelSerializer):
    """Serializer pour les experiences professionnelles."""

    type = serializers.StringRelatedField()
    startDate = serializers.DateField(source="start_date")
    endDate = serializers.DateField(source="end_date", required=False, allow_null=True)
    isCurrent = serializers.BooleanField(source="is_current", read_only=True)

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "company",
            "location",
            "period",
            "startDate",
            "endDate",
            "isCurrent",
            "description",
            "logo",
            "technologies",
            "achievements",
            "type",
        ]


class ExperienceTimelineSerializer(ReadOnlySerializer):
    """Serializer pour la timeline des experiences (lecture seule)."""

    year = serializers.IntegerField(read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)


class ExperienceStatsSerializer(ReadOnlySerializer):
    """Serializer pour les statistiques d'experience (lecture seule)."""

    totalYears = serializers.FloatField(read_only=True)
    companiesCount = serializers.IntegerField(read_only=True)
    topTechnologies = serializers.ListField(child=serializers.DictField(), read_only=True)
    experienceByType = serializers.ListField(child=serializers.DictField(), read_only=True)
