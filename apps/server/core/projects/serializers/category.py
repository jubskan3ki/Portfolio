"""Serializers pour les categories de projets."""

from rest_framework import serializers

from ..models import ProjectCategory


class ProjectCategorySerializer(serializers.ModelSerializer[ProjectCategory]):
    """Serializer pour les categories de projets."""

    count = serializers.SerializerMethodField()

    class Meta:
        model = ProjectCategory
        fields = ("id", "name", "description", "slug", "count")
        read_only_fields = ("id", "slug", "count")

    def get_count(self, obj: ProjectCategory) -> int:
        """Retourne le nombre de projets.

        Uses 'projects_count' annotation when available (list/retrieve).
        Falls back to 0 for single-object responses (create/update)
        where annotation is not present.
        """
        projects_count = getattr(obj, "projects_count", None)
        if projects_count is not None:
            return int(projects_count)
        return 0
