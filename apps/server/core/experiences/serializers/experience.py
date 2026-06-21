"""Serializers pour les experiences professionnelles."""

from django.utils import timezone
from rest_framework import serializers

from utils.serializers import ReadOnlySerializer
from utils.serializers.fields import RelativeMediaFileField

from ..models import Experience, ExperienceType, get_date_order_error


class ExperienceWriteSerializer(serializers.ModelSerializer):
    """Serializer pour la creation et mise a jour des experiences."""

    type = serializers.PrimaryKeyRelatedField(queryset=ExperienceType.objects.all())
    logo = RelativeMediaFileField(required=False, allow_null=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)
    startDate = serializers.DateField(source="start_date", required=False, allow_null=True, write_only=True)
    endDate = serializers.DateField(source="end_date", required=False, allow_null=True, write_only=True)

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "company",
            "location",
            "start_date",
            "end_date",
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
        """Validate dates: start_date requise, pas dans le futur, end_date apres start_date."""
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if not self.partial and not start_date:
            raise serializers.ValidationError({"start_date": "La date de debut est obligatoire."})

        if start_date and start_date > timezone.now().date():
            raise serializers.ValidationError({"start_date": "La date de debut ne peut pas etre dans le futur."})

        date_order_error = get_date_order_error(start_date, end_date)
        if date_order_error:
            raise serializers.ValidationError({"end_date": date_order_error})

        return attrs


class ExperienceSerializer(serializers.ModelSerializer):
    """Serializer pour les experiences professionnelles."""

    type: serializers.StringRelatedField = serializers.StringRelatedField()
    logo = RelativeMediaFileField(read_only=True)
    startDate = serializers.DateField(source="start_date", read_only=True)
    endDate = serializers.DateField(source="end_date", read_only=True)
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
