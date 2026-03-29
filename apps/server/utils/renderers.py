"""Custom DRF renderers."""

from decimal import Decimal

import orjson
from rest_framework.renderers import BaseRenderer


def _default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


class ORJSONRenderer(BaseRenderer):
    """
    DRF renderer using orjson — 2-10x faster than the standard JSONRenderer.
    Supports numpy arrays, dataclasses, UUID, datetime nativement.
    """

    media_type = "application/json"
    format = "json"
    charset = None  # orjson retourne des bytes directement

    def render(self, data, accepted_media_type=None, renderer_context=None):  # noqa: ARG002
        if data is None:
            return b""
        return orjson.dumps(
            data,
            default=_default,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        )
