"""Cache key patterns and TTLs."""

import re
from typing import Any

_UNSAFE_KEY_CHARS = re.compile(r"[\s\x00-\x1f\x7f]")


def _sanitize_part(part: Any) -> str:
    """Remplace les caracteres interdits (espaces, controle) par '_'."""
    return _UNSAFE_KEY_CHARS.sub("_", str(part))


class CacheKeys:
    """Cache key factory; prefixe + version pour invalidation globale."""

    PREFIX = "portfolio"
    VERSION = "v1"

    TTL_SHORT = 60
    TTL_MEDIUM = 300
    TTL_LONG = 3600
    TTL_DAY = 86400

    @classmethod
    def article_featured(cls, limit: int = 5) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:articles:featured:{limit}"

    @classmethod
    def article_popular(cls, limit: int = 5) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:articles:popular:{limit}"

    @classmethod
    def article_recent(cls, limit: int = 5) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:articles:recent:{limit}"

    @classmethod
    def article_detail(cls, slug: str) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:articles:detail:{slug}"

    @classmethod
    def article_categories(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:articles:categories"

    @classmethod
    def article_tags(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:articles:tags"

    @classmethod
    def project_featured(cls, limit: int = 5) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:projects:featured:{limit}"

    @classmethod
    def project_list(cls, category: str = "all") -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:projects:list:{category}"

    @classmethod
    def project_detail(cls, slug: str) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:projects:detail:{slug}"

    @classmethod
    def project_categories(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:projects:categories"

    @classmethod
    def stack_list(cls, category: str = "all") -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:stacks:list:{category}"

    @classmethod
    def stack_detail(cls, slug: str) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:stacks:detail:{slug}"

    @classmethod
    def stack_categories(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:stacks:categories"

    @classmethod
    def experience_timeline(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:experiences:timeline"

    @classmethod
    def experience_types(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:experiences:types"

    @classmethod
    def stats_global(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:stats:global"

    @classmethod
    def pattern_articles(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:articles:*"

    @classmethod
    def pattern_projects(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:projects:*"

    @classmethod
    def pattern_stacks(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:stacks:*"

    @classmethod
    def pattern_experiences(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:experiences:*"

    @classmethod
    def pattern_all(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}:*"

    @classmethod
    def make_key(cls, *parts: Any) -> str:
        parts_str = ":".join(_sanitize_part(p) for p in parts)
        return f"{cls.PREFIX}:{cls.VERSION}:{parts_str}"
