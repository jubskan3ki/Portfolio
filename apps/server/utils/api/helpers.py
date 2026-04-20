"""Helpers pour les API views."""

from config.constants import DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT, MIN_PAGE_LIMIT


def parse_limit(
    value: str | int | None,
    default: int = DEFAULT_PAGE_LIMIT,
    min_limit: int = MIN_PAGE_LIMIT,
    max_limit: int = MAX_PAGE_LIMIT,
) -> int:
    """Parse limit en clampant entre min et max."""
    if value is None:
        return default

    try:
        limit = int(value)
        return max(min_limit, min(limit, max_limit))
    except (ValueError, TypeError):
        return default


def parse_page(value: str | int | None, default: int = 1) -> int:
    if value is None:
        return default

    try:
        page = int(value)
        return max(1, page)
    except (ValueError, TypeError):
        return default


def parse_bool(value: str | None, *, default: bool = False) -> bool:
    """Accepte 'true'/'1'/'yes'/'on' (case-insensitive)."""
    if value is None:
        return default

    return str(value).lower() in ("true", "1", "yes", "on")


def parse_sort_direction(value: str | None, default: str = "desc") -> str:
    if value is None:
        return default

    value_lower = str(value).lower()
    if value_lower in ("asc", "ascending", "1"):
        return "asc"
    if value_lower in ("desc", "descending", "-1"):
        return "desc"
    return default


def get_ordering_prefix(direction: str) -> str:
    """'' pour asc, '-' pour desc."""
    return "" if direction == "asc" else "-"


def safe_get_param(
    params: dict[str, str],
    key: str,
    default: str | int | None = None,
    param_type: type = str,
) -> str | int | bool | None:
    """Recupere un query param avec conversion de type (str/int/bool)."""
    value = params.get(key)
    if value is None:
        return default

    try:
        if param_type is bool:
            return parse_bool(value, default=default if isinstance(default, bool) else False)
        if param_type is int:
            return int(value)
        return param_type(value)
    except (ValueError, TypeError):
        return default
