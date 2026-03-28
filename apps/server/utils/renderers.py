"""Custom DRF renderers."""

import orjson
from rest_framework.renderers import BaseRenderer


class ORJSONRenderer(BaseRenderer):
    """
    DRF renderer using orjson — 2-10x faster than the standard JSONRenderer.
    Supports numpy arrays, dataclasses, UUID, datetime nativement.
    """

    media_type = "application/json"
    format = "json"
    charset = None  # orjson retourne des bytes directement

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b""
        return orjson.dumps(
            data,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        )
