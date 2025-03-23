"""
Sérialisation des articles de blog.
"""

from django.utils import timezone
from django.utils.text import slugify
from rest_framework import serializers

from ..models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    """
    Sérialisation complète des articles de blog avec validations avancées et champs calculés.
    """

    is_published = serializers.ReadOnlyField()
    views_count = serializers.ReadOnlyField()

    class Meta:
        """
        Métadonnées du sérialiseur.
        """

        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "image",
            "category",
            "tags",
            "author",
            "status",
            "published_at",
            "meta_description",
            "seo_keywords",
            "views_count",
            "is_published",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        """
        Le titre doit contenir au moins 5 caractères.
        """
        title = value.strip()
        if len(title) < 5:
            raise serializers.ValidationError("Le titre doit contenir au moins 5 caractères.")
        return title

    def validate_meta_description(self, value):
        """
        Vérifie que la méta-description ne dépasse pas 160 caractères.
        """
        if value and len(value) > 160:
            raise serializers.ValidationError("La méta-description ne peut dépasser 160 caractères.")
        return value.strip()

    def validate_image(self, value):
        """
        Limitation stricte de la taille de l'image (2 Mo max).
        """
        max_size = 2 * 1024 * 1024
        if value and value.size > max_size:
            raise serializers.ValidationError("L'image ne doit pas dépasser 2 Mo.")
        return value

    def validate_tags(self, value):
        """
        Assure que les tags sont fournis sous forme de liste.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Les tags doivent être une liste.")
        return value

    def validate_seo_keywords(self, value):
        """
        Vérifie que les mots-clés SEO sont une liste avec au maximum 10 mots-clés.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Les mots-clés SEO doivent être une liste.")
        if len(value) > 10:
            raise serializers.ValidationError("Vous ne pouvez spécifier plus de 10 mots-clés SEO.")
        return value

    def validate(self, attrs):
        """
        Vérifie que published_at est renseigné si l'article est publié.
        """
        status = attrs.get("status")
        published_at = attrs.get("published_at", None)

        if status == "published" and not published_at:
            attrs["published_at"] = timezone.now()

        return attrs

    def create(self, validated_data):
        """
        Génère automatiquement un slug à partir du titre à la création.
        """
        validated_data.setdefault("slug", slugify(validated_data["title"]))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Met à jour automatiquement le slug si le titre change.
        """
        if "title" in validated_data:
            validated_data["slug"] = slugify(validated_data["title"])
        return super().update(instance, validated_data)
