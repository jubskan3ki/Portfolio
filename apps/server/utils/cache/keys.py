"""Cache key patterns and utilities."""

from typing import Any


class CacheKeys:
    """
    Centralized cache key patterns.

    Usage:
        key = CacheKeys.article_featured(limit=5)
        key = CacheKeys.project_list(category="web")
    """

    # Prefixes
    PREFIX = "portfolio"
    VERSION = "v1"

    # TTL values (in seconds)
    TTL_SHORT = 60  # 1 minute
    TTL_MEDIUM = 300  # 5 minutes
    TTL_LONG = 3600  # 1 hour
    TTL_DAY = 86400  # 24 hours

    # === Articles ===

    @classmethod
    def article_featured(cls, limit: int = 5) -> str:
        """Cache key for featured articles."""
        return f"{cls.PREFIX}:{cls.VERSION}:articles:featured:{limit}"

    @classmethod
    def article_popular(cls, limit: int = 5) -> str:
        """Cache key for popular articles."""
        return f"{cls.PREFIX}:{cls.VERSION}:articles:popular:{limit}"

    @classmethod
    def article_recent(cls, limit: int = 5) -> str:
        """Cache key for recent articles."""
        return f"{cls.PREFIX}:{cls.VERSION}:articles:recent:{limit}"

    @classmethod
    def article_detail(cls, slug: str) -> str:
        """Cache key for article detail."""
        return f"{cls.PREFIX}:{cls.VERSION}:articles:detail:{slug}"

    @classmethod
    def article_categories(cls) -> str:
        """Cache key for article categories."""
        return f"{cls.PREFIX}:{cls.VERSION}:articles:categories"

    @classmethod
    def article_tags(cls) -> str:
        """Cache key for article tags."""
        return f"{cls.PREFIX}:{cls.VERSION}:articles:tags"

    # === Projects ===

    @classmethod
    def project_featured(cls, limit: int = 5) -> str:
        """Cache key for featured projects."""
        return f"{cls.PREFIX}:{cls.VERSION}:projects:featured:{limit}"

    @classmethod
    def project_list(cls, category: str = "all") -> str:
        """Cache key for project list by category."""
        return f"{cls.PREFIX}:{cls.VERSION}:projects:list:{category}"

    @classmethod
    def project_detail(cls, slug: str) -> str:
        """Cache key for project detail."""
        return f"{cls.PREFIX}:{cls.VERSION}:projects:detail:{slug}"

    @classmethod
    def project_categories(cls) -> str:
        """Cache key for project categories."""
        return f"{cls.PREFIX}:{cls.VERSION}:projects:categories"

    # === Stacks ===

    @classmethod
    def stack_list(cls, category: str = "all") -> str:
        """Cache key for stack list by category."""
        return f"{cls.PREFIX}:{cls.VERSION}:stacks:list:{category}"

    @classmethod
    def stack_detail(cls, slug: str) -> str:
        """Cache key for stack detail."""
        return f"{cls.PREFIX}:{cls.VERSION}:stacks:detail:{slug}"

    @classmethod
    def stack_categories(cls) -> str:
        """Cache key for stack categories."""
        return f"{cls.PREFIX}:{cls.VERSION}:stacks:categories"

    # === Experiences ===

    @classmethod
    def experience_timeline(cls) -> str:
        """Cache key for experience timeline."""
        return f"{cls.PREFIX}:{cls.VERSION}:experiences:timeline"

    @classmethod
    def experience_types(cls) -> str:
        """Cache key for experience types."""
        return f"{cls.PREFIX}:{cls.VERSION}:experiences:types"

    # === Stats ===

    @classmethod
    def stats_global(cls) -> str:
        """Cache key for global stats."""
        return f"{cls.PREFIX}:{cls.VERSION}:stats:global"

    # === Patterns for invalidation ===

    @classmethod
    def pattern_articles(cls) -> str:
        """Pattern to match all article cache keys."""
        return f"{cls.PREFIX}:{cls.VERSION}:articles:*"

    @classmethod
    def pattern_projects(cls) -> str:
        """Pattern to match all project cache keys."""
        return f"{cls.PREFIX}:{cls.VERSION}:projects:*"

    @classmethod
    def pattern_stacks(cls) -> str:
        """Pattern to match all stack cache keys."""
        return f"{cls.PREFIX}:{cls.VERSION}:stacks:*"

    @classmethod
    def pattern_experiences(cls) -> str:
        """Pattern to match all experience cache keys."""
        return f"{cls.PREFIX}:{cls.VERSION}:experiences:*"

    @classmethod
    def pattern_all(cls) -> str:
        """Pattern to match all cache keys."""
        return f"{cls.PREFIX}:{cls.VERSION}:*"

    @classmethod
    def make_key(cls, *parts: Any) -> str:
        """Create a custom cache key from parts."""
        parts_str = ":".join(str(p) for p in parts)
        return f"{cls.PREFIX}:{cls.VERSION}:{parts_str}"
