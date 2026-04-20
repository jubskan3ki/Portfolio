"""Custom DRF renderers."""

from decimal import Decimal

import orjson
from rest_framework.renderers import BaseRenderer


def _default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


class ORJSONRenderer(BaseRenderer):
    """DRF renderer orjson : 2-10x plus rapide, supporte UUID/datetime/numpy nativement."""

    media_type = "application/json"
    format = "json"
    charset = None  # orjson retourne bytes

    def render(self, data, accepted_media_type=None, renderer_context=None):  # noqa: ARG002
        if data is None:
            return b""
        return orjson.dumps(
            data,
            default=_default,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        )


class ProblemDetailRenderer(ORJSONRenderer):
    """RFC 7807 : application/problem+json (meme serialisation qu'ORJSONRenderer)."""

    media_type = "application/problem+json"
    format = "problem+json"
