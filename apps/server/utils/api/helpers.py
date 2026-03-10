"""Helpers centralises pour les API views."""

from config.constants import (
    DEFAULT_PAGE_LIMIT,
    MAX_PAGE_LIMIT,
    MIN_PAGE_LIMIT,
)


def parse_limit(
    value: str | int | None,
    default: int = DEFAULT_PAGE_LIMIT,
    min_limit: int = MIN_PAGE_LIMIT,
    max_limit: int = MAX_PAGE_LIMIT,
) -> int:
    """Parse et valide une valeur de limit pour la pagination.

    Args:
        value: Valeur a parser (string ou int)
        default: Valeur par defaut si parsing echoue
        min_limit: Valeur minimum autorisee
        max_limit: Valeur maximum autorisee

    Returns:
        Valeur de limit validee entre min et max
    """
    if value is None:
        return default

    try:
        limit = int(value)
        return max(min_limit, min(limit, max_limit))
    except (ValueError, TypeError):
        return default


def parse_page(value: str | int | None, default: int = 1) -> int:
    """Parse et valide un numero de page.

    Args:
        value: Valeur a parser
        default: Valeur par defaut (1)

    Returns:
        Numero de page valide (minimum 1)
    """
    if value is None:
        return default

    try:
        page = int(value)
        return max(1, page)
    except (ValueError, TypeError):
        return default


def parse_bool(
    value: str | bool | None,  # noqa: FBT001
    default: bool = False,  # noqa: FBT001, FBT002
) -> bool:
    """Parse une valeur booleenne depuis query params.

    Args:
        value: Valeur a parser ('true', 'false', '1', '0', etc.)
        default: Valeur par defaut

    Returns:
        Valeur booleenne
    """
    if value is None:
        return default

    if isinstance(value, bool):
        return value

    return str(value).lower() in ("true", "1", "yes", "on")


def parse_sort_direction(value: str | None, default: str = "desc") -> str:
    """Parse et valide une direction de tri.

    Args:
        value: 'asc' ou 'desc'
        default: Direction par defaut

    Returns:
        'asc' ou 'desc'
    """
    if value is None:
        return default

    value_lower = str(value).lower()
    if value_lower in ("asc", "ascending", "1"):
        return "asc"
    if value_lower in ("desc", "descending", "-1"):
        return "desc"
    return default


def get_ordering_prefix(direction: str) -> str:
    """Retourne le prefixe Django pour le tri.

    Args:
        direction: 'asc' ou 'desc'

    Returns:
        '' pour asc, '-' pour desc
    """
    return "" if direction == "asc" else "-"


def safe_get_param(
    params: dict[str, str],
    key: str,
    default: str | int | None = None,
    param_type: type = str,
) -> str | int | bool | None:
    """Recupere un parametre de maniere securisee avec conversion de type.

    Args:
        params: Dictionnaire de parametres (query_params)
        key: Cle a recuperer
        default: Valeur par defaut
        param_type: Type de conversion (str, int, bool)

    Returns:
        Valeur convertie ou default
    """
    value = params.get(key)
    if value is None:
        return default

    try:
        if param_type is bool:
            return parse_bool(value, default if isinstance(default, bool) else False)
        if param_type is int:
            return int(value)
        return param_type(value)
    except (ValueError, TypeError):
        return default
