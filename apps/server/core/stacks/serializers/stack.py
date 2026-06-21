"""Serializers pour les stacks techniques."""

from typing import Any, cast

from rest_framework import serializers

from utils.serializers.fields import RelativeMediaFileField
from utils.validators import validate_string_list

from ..models import Stack, StackCategory, StackRelationship
from .resource import StackResourceSerializer


class RelatedStackSerializer(serializers.ModelSerializer):
    """Serializer pour les stacks associees (version legere)."""

    category: serializers.StringRelatedField = serializers.StringRelatedField()
    logo = RelativeMediaFileField(read_only=True)
    relationship = serializers.SerializerMethodField()

    class Meta:
        model = Stack
        fields = ("name", "logo", "slug", "category", "relationship")

    def get_relationship(self, obj: Stack) -> str:
        """Recupere le type de relation depuis le contexte."""
        relationships = self.context.get("relationships", {})
        return relationships.get(obj.pk, "similarTo")


class StackListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des stacks (version allegee)."""

    category: serializers.StringRelatedField = serializers.StringRelatedField()
    logo = RelativeMediaFileField(read_only=True)
    experience = serializers.SerializerMethodField()

    class Meta:
        model = Stack
        fields = (
            "id",
            "name",
            "logo",
            "category",
            "slug",
            "description",
            "experience",
            "level",
            "tags",
            "started_date",
        )
        read_only_fields = ("id", "slug", "experience")

    def get_experience(self, obj: Stack) -> int:
        """Retourne l'experience en mois depuis la date de debut."""
        return obj.experience_months


class StackDetailSerializer(serializers.ModelSerializer):
    """Serializer pour les details d'une stack (lecture seule)."""

    category: serializers.StringRelatedField = serializers.StringRelatedField()
    logo = RelativeMediaFileField(read_only=True)
    resources = StackResourceSerializer(many=True, read_only=True)
    related_stacks = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()

    seoTitle = serializers.CharField(source="seo_title", read_only=True)
    metaDescription = serializers.CharField(source="meta_description", read_only=True)

    class Meta:
        model = Stack
        fields = (
            "id",
            "name",
            "slug",
            "seoTitle",
            "metaDescription",
            "description",
            "logo",
            "category",
            "tags",
            "started_date",
            "experience",
            "level",
            "website",
            "website_label",
            "github",
            "github_label",
            "first_release",
            "license",
            "content",
            "resources",
            "related_stacks",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields

    def get_experience(self, obj: Stack) -> int:
        """Retourne l'experience en mois depuis la date de debut."""
        return obj.experience_months

    def get_related_stacks(self, obj: Stack) -> list[dict[str, Any]]:
        """Recupere les stacks associees avec leurs relations.

        Delegue a RelatedStackSerializer (source unique du dict de sortie) ;
        le type de relation transite par le contexte {pk: relationship_type}.
        """
        qs = getattr(obj, "relationships", StackRelationship.objects.none())
        related_stacks: list[Stack] = []
        relationship_map: dict[Any, str] = {}
        for rel in qs.all():
            related_stacks.append(rel.to_stack)
            relationship_map[rel.to_stack.pk] = rel.relationship_type

        return cast(
            list[dict[str, Any]],
            RelatedStackSerializer(
                related_stacks,
                many=True,
                context={"relationships": relationship_map},
            ).data,
        )


class StackWriteSerializer(serializers.ModelSerializer):
    """Serializer pour la creation et mise a jour des stacks."""

    category = serializers.PrimaryKeyRelatedField(
        queryset=StackCategory.objects.all(),
    )
    logo = RelativeMediaFileField(required=False, allow_null=True)

    class Meta:
        model = Stack
        fields = (
            "id",
            "name",
            "slug",
            "seo_title",
            "meta_description",
            "description",
            "logo",
            "category",
            "tags",
            "started_date",
            "level",
            "website",
            "website_label",
            "github",
            "github_label",
            "first_release",
            "license",
            "content",
        )
        read_only_fields = ("id",)
        extra_kwargs = {
            "slug": {"required": False},
            "seo_title": {"required": False, "allow_blank": True},
            "meta_description": {"required": False, "allow_blank": True},
            "description": {"required": False, "allow_blank": True},
            "logo": {"required": False},
            "tags": {"required": False, "default": list},
            "started_date": {"required": False, "allow_null": True},
            "website": {"required": False, "allow_blank": True},
            "website_label": {"required": False, "allow_blank": True},
            "github": {"required": False, "allow_blank": True},
            "github_label": {"required": False, "allow_blank": True},
            "first_release": {"required": False, "allow_blank": True},
            "license": {"required": False, "allow_blank": True},
            "content": {"required": False, "allow_blank": True},
        }

    def validate_category(self, value: StackCategory | None) -> StackCategory:
        """Valide que la categorie existe."""
        if not value:
            raise serializers.ValidationError("La categorie est obligatoire.")
        return value

    def validate_tags(self, value):
        """Valide que tags est une liste de strings."""
        return validate_string_list(value, item_label="tag")
