"""PG tsquery avec prefix matching `:*` (websearch_to_tsquery ne gere que mot exact post-stemming)."""

from __future__ import annotations

import re

_TOKEN_RE = re.compile(r"\w+", re.UNICODE)
_MIN_TOKEN_LENGTH = 1


def build_prefix_tsquery(user_query: str) -> str:
    """ "nux django" -> "nux:* & django:*". Prefix matching des 1 caractere."""
    tokens = [t.lower() for t in _TOKEN_RE.findall(user_query or "") if len(t) >= _MIN_TOKEN_LENGTH]
    if not tokens:
        return ""
    return " & ".join(f"{token}:*" for token in tokens)
