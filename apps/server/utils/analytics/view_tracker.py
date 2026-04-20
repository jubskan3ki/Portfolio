"""View tracking with Redis buffering for performance optimization."""

import logging
from typing import Literal, cast

from django.core.cache import cache
from django.db import transaction
from django.db.models import F

logger = logging.getLogger("core.analytics")

ContentType = Literal["article", "project", "stack"]


class ViewTracker:
    """Buffer vues en Redis (flush au seuil) pour reduire les ecritures DB."""

    BUFFER_KEY_PREFIX = "view_buffer"
    FLUSH_THRESHOLD = 10
    BUFFER_TTL = 3600  # fallback si flush jamais declenche

    MODELS = {
        "article": ("core.articles.models", "Article"),
        "project": ("core.projects.models", "Project"),
        "stack": ("core.stacks.models", "Stack"),
    }

    @classmethod
    def _get_buffer_key(cls, content_type: ContentType, object_id: int) -> str:
        return f"{cls.BUFFER_KEY_PREFIX}:{content_type}:{object_id}"

    @classmethod
    def _get_model(cls, content_type: ContentType):
        if content_type not in cls.MODELS:
            raise ValueError(f"Unknown content type: {content_type}")

        module_path, class_name = cls.MODELS[content_type]

        from importlib import import_module

        module = import_module(module_path)
        return getattr(module, class_name)

    @classmethod
    def increment(cls, content_type: ContentType, object_id: int) -> int:
        """Incremente le compteur buffer; flush auto au seuil."""
        key = cls._get_buffer_key(content_type, object_id)

        try:
            count = 1 if cache.add(key, 1, cls.BUFFER_TTL) else cache.incr(key)

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
            cls._update_db(content_type, object_id, 1)
            return 0

    @classmethod
    def flush(cls, content_type: ContentType, object_id: int) -> int:
        """Flush vers la DB; retourne le nombre flushe."""
        key = cls._get_buffer_key(content_type, object_id)

        count = cache.get(key, 0)
        if not count:
            return 0

        cache.delete(key)

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
        flushed: dict[str, int] = {}
        pattern = f"{cls.BUFFER_KEY_PREFIX}:*"

        try:
            if hasattr(cache, "keys"):
                keys = cache.keys(pattern)
            else:
                logger.warning("Cache backend doesn't support keys() method")
                return flushed

            for key in keys:
                try:
                    # key format: view_buffer:content_type:object_id
                    parts = key.split(":")
                    if len(parts) != 3:
                        continue

                    _, content_type_str, object_id = parts
                    if content_type_str not in cls.MODELS:
                        logger.warning("Unknown content type in buffer key: %s", content_type_str)
                        continue
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
        key = cls._get_buffer_key(content_type, object_id)
        return cache.get(key, 0)

    @classmethod
    def get_total_count(cls, content_type: ContentType, object_id: int) -> int:
        """DB + buffer."""
        try:
            model = cls._get_model(content_type)
            obj = model.objects.filter(pk=object_id).values("view_count").first()
            db_count = obj["view_count"] if obj else 0
            buffer_count = cls.get_buffered_count(content_type, object_id)
            return db_count + buffer_count
        except Exception:
            logger.exception("Failed to get total count for %s:%s", content_type, object_id)
            return 0
