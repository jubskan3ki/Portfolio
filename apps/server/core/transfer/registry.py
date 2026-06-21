"""Registre centralise des modules supportes par le systeme de transfer."""

from typing import Any

MODULE_REGISTRY: dict[str, dict[str, Any]] = {
    "articles": {
        "app_label": "articles",
        "model_name": "Article",
        "serializer_module": "core.articles.serializers",
        "serializer_name": "ArticleDetailSerializer",
        "select_related": ["category"],
        "prefetch_related": ["tags"],
        "required_fields": ["title", "excerpt", "category"],
    },
    "projects": {
        "app_label": "projects",
        "model_name": "Project",
        "serializer_module": "core.projects.serializers",
        "serializer_name": "ProjectDetailSerializer",
        "select_related": ["category", "status"],
        "prefetch_related": [],
        "required_fields": ["title", "description", "category"],
    },
    "stacks": {
        "app_label": "stacks",
        "model_name": "Stack",
        "serializer_module": "core.stacks.serializers",
        "serializer_name": "StackDetailSerializer",
        "select_related": ["category"],
        "prefetch_related": ["resources", "relationships__to_stack__category"],
        "required_fields": ["name", "category", "description", "level"],
    },
    "experiences": {
        "app_label": "experiences",
        "model_name": "Experience",
        "serializer_module": "core.experiences.serializers",
        "serializer_name": "ExperienceSerializer",
        "select_related": ["type"],
        "prefetch_related": [],
        "required_fields": ["title", "company", "start_date", "type", "location", "description"],
    },
    "contacts": {
        "app_label": "contact",
        "model_name": "Contact",
        "serializer_module": "core.contact.serializers",
        "serializer_name": "ContactSerializer",
        "select_related": [],
        "prefetch_related": [],
        "required_fields": ["name", "email", "subject", "message"],
    },
}

SUPPORTED_MODULES = list(MODULE_REGISTRY.keys())
