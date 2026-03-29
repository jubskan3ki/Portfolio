"""Serializers pour les projets."""

from rest_framework import serializers

from utils.serializers.fields import URLDictField
from utils.validators import validate_string_list

from ..models import Project, ProjectCategory, ProjectStatus


class ProjectWriteSerializer(serializers.ModelSerializer[Project]):
    """Serializer pour la creation et mise a jour des projets."""

    category = serializers.PrimaryKeyRelatedField(queryset=ProjectCategory.objects.all())
    status = serializers.PrimaryKeyRelatedField(
        queryset=ProjectStatus.objects.all(),
        required=False,
        allow_null=True,
    )
    long_description = serializers.CharField(required=False, allow_blank=True)
    # Accept longDescription from frontend and map to long_description
    longDescription = serializers.CharField(
        source="long_description",
        required=False,
        allow_blank=True,
        write_only=True,
    )

    links = URLDictField(
        allowed_keys={"demo", "github", "documentation", "website"},
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "long_description",
            "longDescription",
            "image",
            "category",
            "status",
            "technologies",
            "features",
            "links",
            "date",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "slug": {"required": False},
            "technologies": {"required": False},
            "features": {"required": False},
            "date": {"required": False},
        }

    def validate_technologies(self, value):
        """Valide que technologies est une liste de strings."""
        return validate_string_list(value, item_label="technologie")

    def validate_features(self, value):
        """Valide que features est une liste de strings."""
        return validate_string_list(value, item_label="fonctionnalite")


class ProjectListSerializer(serializers.ModelSerializer[Project]):
    """Serializer pour la liste des projets (version allegee)."""

    category = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    views = serializers.IntegerField(source="view_count", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "image",
            "category",
            "status",
            "technologies",
            "date",
            "updatedAt",
            "views",
        )


class ProjectDetailSerializer(serializers.ModelSerializer[Project]):
    """Serializer pour les details d'un projet."""

    category = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    views = serializers.IntegerField(source="view_count", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    seoTitle = serializers.CharField(source="seo_title", read_only=True)
    metaDescription = serializers.CharField(source="meta_description", read_only=True)
    longDescription = serializers.CharField(source="long_description")

    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "slug",
            "seoTitle",
            "metaDescription",
            "description",
            "views",
            "longDescription",
            "status",
            "image",
            "category",
            "technologies",
            "date",
            "updatedAt",
            "features",
            "links",
        )
        read_only_fields = ("id", "slug", "view")
