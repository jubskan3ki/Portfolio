"""Serialiseurs pour les articles."""

from typing import Any

from rest_framework import serializers

from utils.serializers.fields import JSONBlockListField

from ..models import Article, Category, Tag
from ..services.article import ArticleService


class ArticleWriteSerializer(serializers.ModelSerializer):
    """Serialiseur pour la creation et mise a jour des articles."""

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    content = JSONBlockListField(required=False, default=list)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "seo_title",
            "meta_description",
            "excerpt",
            "content",
            "image",
            "category",
            "tags",
            "read_time",
            "is_published",
            "is_featured",
        ]
        read_only_fields = ["id", "is_featured"]
        extra_kwargs = {
            "slug": {"required": False},
            "seo_title": {"required": False, "allow_blank": True},
            "meta_description": {"required": False, "allow_blank": True},
            "excerpt": {"required": False, "allow_blank": True},
            "image": {"required": False},
            "read_time": {"required": False},
            "is_featured": {"required": False},
        }

    def create(self, validated_data: dict[str, Any]) -> Article:
        """Delegue la creation a ArticleService (publication auto)."""
        tags = validated_data.pop("tags", [])
        tag_names = [tag.name for tag in tags] if tags else None

        data = {**validated_data}
        if tag_names:
            data["tags"] = tag_names

        return ArticleService.create(data)

    def update(self, instance: Article, validated_data: dict[str, Any]) -> Article:
        """Delegue la mise a jour a ArticleService (publication auto)."""
        tags = validated_data.pop("tags", None)
        tag_names = [tag.name for tag in tags] if tags is not None else None

        data = {**validated_data}
        if tag_names is not None:
            data["tags"] = tag_names

        return ArticleService.update(instance.id, data)


class _ArticleReadFieldsMixin(serializers.Serializer):
    """Champs de lecture communs aux serialiseurs liste et detail."""

    category = serializers.StringRelatedField()
    tags = serializers.SerializerMethodField()
    date = serializers.DateTimeField(source="published_date")
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    seoTitle = serializers.CharField(source="seo_title", read_only=True)
    metaDescription = serializers.CharField(source="meta_description", read_only=True)
    readTime = serializers.IntegerField(source="read_time")
    views = serializers.IntegerField(source="view_count")

    def get_tags(self, obj: Article) -> list[str]:
        """Retourne la liste des noms de tags."""
        return obj.tag_list


class ArticleListSerializer(_ArticleReadFieldsMixin, serializers.ModelSerializer):
    """Serialiseur pour la liste des articles."""

    is_published = serializers.BooleanField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "image",
            "category",
            "tags",
            "date",
            "updatedAt",
            "readTime",
            "views",
            "is_published",
        ]


class ArticleDetailSerializer(_ArticleReadFieldsMixin, serializers.ModelSerializer):
    """Serialiseur pour les details d'un article."""

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "seoTitle",
            "metaDescription",
            "excerpt",
            "content",
            "image",
            "category",
            "tags",
            "date",
            "updatedAt",
            "readTime",
            "views",
            "is_published",
        ]
