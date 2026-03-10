"""View tracking with Redis buffering for performance optimization."""

import logging
from typing import Literal, cast

from django.core.cache import cache
from django.db import transaction
from django.db.models import F

logger = logging.getLogger("core.analytics")

ContentType = Literal["article", "project", "stack"]


class ViewTracker:
    """
    Buffered view counter using Redis to reduce database writes.

    Instead of updating the database on every view, this class:
    1. Buffers view counts in Redis
    2. Flushes to the database when threshold is reached or manually triggered
    3. Provides atomic operations for thread safety

    Usage:
        # Increment view (buffered)
        ViewTracker.increment("article", article.id)

        # Force flush specific content
        ViewTracker.flush("article", article.id)

        # Flush all buffered views
        ViewTracker.flush_all()
    """

    # Buffer settings
    BUFFER_KEY_PREFIX = "view_buffer"
    FLUSH_THRESHOLD = 10  # Flush to DB after this many views
    BUFFER_TTL = 3600  # Buffer expires after 1 hour (fallback)

    # Model mapping
    MODELS = {
        "article": ("core.articles.models", "Article"),
        "project": ("core.projects.models", "Project"),
        "stack": ("core.stacks.models", "Stack"),
    }

    @classmethod
    def _get_buffer_key(cls, content_type: ContentType, object_id: int) -> str:
        """Generate cache key for buffered views."""
        return f"{cls.BUFFER_KEY_PREFIX}:{content_type}:{object_id}"

    @classmethod
    def _get_model(cls, content_type: ContentType):
        """Get the model class for the content type."""
        if content_type not in cls.MODELS:
            raise ValueError(f"Unknown content type: {content_type}")

        module_path, class_name = cls.MODELS[content_type]

        # Dynamic import
        from importlib import import_module

        module = import_module(module_path)
        return getattr(module, class_name)

    @classmethod
    def increment(cls, content_type: ContentType, object_id: int) -> int:
        """
        Increment view count for content.

        Returns the new buffered count.
        """
        key = cls._get_buffer_key(content_type, object_id)

        try:
            # Key was just created with value 1, or increment existing key
            count = 1 if cache.add(key, 1, cls.BUFFER_TTL) else cache.incr(key)

            # Check if we should flush
            if count >= cls.FLUSH_THRESHOLD:
                cls.flush(content_type, object_id)
                return 0

            return count

        except Exception as e:
            logger.warning(
                "Failed to buffer view for %s:%s - falling back to direct DB update: %s",
                content_type,
                object_id,
                e,
            )
            # Fallback: direct database update
            cls._update_db(content_type, object_id, 1)
            return 0

    @classmethod
    def flush(cls, content_type: ContentType, object_id: int) -> int:
        """
        Flush buffered views to the database.

        Returns the number of views flushed.
        """
        key = cls._get_buffer_key(content_type, object_id)

        # Get and delete atomically (if supported)
        count = cache.get(key, 0)
        if not count:
            return 0

        cache.delete(key)

        # Update database
        if count > 0:
            cls._update_db(content_type, object_id, count)
            logger.debug(
                "Flushed %d views for %s:%s",
                count,
                content_type,
                object_id,
            )

        return count

    @classmethod
    def _update_db(cls, content_type: ContentType, object_id: int, count: int) -> None:
        """Update the database view count atomically."""
        try:
            model = cls._get_model(content_type)
            with transaction.atomic():
                model.objects.filter(pk=object_id).update(view_count=F("view_count") + count)
        except Exception:
            logger.exception(
                "Failed to update view count for %s:%s",
                content_type,
                object_id,
            )

    @classmethod
    def flush_all(cls) -> dict[str, int]:
        """
        Flush all buffered views to the database.

        Returns a dict of {content_type:object_id: count_flushed}
        """
        flushed: dict[str, int] = {}
        pattern = f"{cls.BUFFER_KEY_PREFIX}:*"

        try:
            # Get all buffer keys
            if hasattr(cache, "keys"):
                keys = cache.keys(pattern)
            else:
                logger.warning("Cache backend doesn't support keys() method")
                return flushed

            for key in keys:
                try:
                    # Parse key: view_buffer:content_type:object_id
                    parts = key.split(":")
                    if len(parts) != 3:
                        continue

                    _, content_type_str, object_id = parts
                    # Validate content type before calling flush
                    if content_type_str not in cls.MODELS:
                        logger.warning("Unknown content type in buffer key: %s", content_type_str)
                        continue
                    # Cast is safe after validation above
                    count = cls.flush(cast(ContentType, content_type_str), int(object_id))
                    if count > 0:
                        flushed[f"{content_type_str}:{object_id}"] = count

                except (ValueError, TypeError) as e:
                    logger.warning("Failed to parse buffer key %s: %s", key, e)

        except Exception:
            logger.exception("Failed to flush all views")

        if flushed:
            logger.info("Flushed views: %s", flushed)

        return flushed

    @classmethod
    def get_buffered_count(cls, content_type: ContentType, object_id: int) -> int:
        """Get the current buffered (not yet flushed) view count."""
        key = cls._get_buffer_key(content_type, object_id)
        return cache.get(key, 0)

    @classmethod
    def get_total_count(cls, content_type: ContentType, object_id: int) -> int:
        """Get total view count (database + buffer)."""
        try:
            model = cls._get_model(content_type)
            obj = model.objects.filter(pk=object_id).values("view_count").first()
            db_count = obj["view_count"] if obj else 0
            buffer_count = cls.get_buffered_count(content_type, object_id)
            return db_count + buffer_count
        except Exception:
            logger.exception("Failed to get total count for %s:%s", content_type, object_id)
            return 0
