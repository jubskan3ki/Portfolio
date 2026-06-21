"""Django settings dispatcher. Loads modular settings, then DJANGO_ENV overrides."""

import importlib
import os
from types import ModuleType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config.settings.base import ALLOWED_AVATAR_EXTENSIONS as ALLOWED_AVATAR_EXTENSIONS
    from config.settings.base import BASE_DIR as BASE_DIR
    from config.settings.base import MAX_AVATAR_SIZE as MAX_AVATAR_SIZE
    from config.settings.email import ADMIN_EMAIL as ADMIN_EMAIL
    from config.settings.jwt import AUTH_COOKIE_ACCESS as AUTH_COOKIE_ACCESS
    from config.settings.jwt import AUTH_COOKIE_ACCESS_MAX_AGE as AUTH_COOKIE_ACCESS_MAX_AGE
    from config.settings.jwt import AUTH_COOKIE_DOMAIN as AUTH_COOKIE_DOMAIN
    from config.settings.jwt import AUTH_COOKIE_HTTP_ONLY as AUTH_COOKIE_HTTP_ONLY
    from config.settings.jwt import AUTH_COOKIE_PATH as AUTH_COOKIE_PATH
    from config.settings.jwt import AUTH_COOKIE_REFRESH as AUTH_COOKIE_REFRESH
    from config.settings.jwt import AUTH_COOKIE_REFRESH_MAX_AGE as AUTH_COOKIE_REFRESH_MAX_AGE
    from config.settings.jwt import AUTH_COOKIE_SAMESITE as AUTH_COOKIE_SAMESITE
    from config.settings.jwt import AUTH_COOKIE_SECURE as AUTH_COOKIE_SECURE

_BASE_MODULES = (
    "base",
    "cache",
    "celery_conf",
    "database",
    "email",
    "jwt",
    "logging_conf",
    "rest_framework",
    "security",
    "storage",
)

for _name in _BASE_MODULES:
    _module = importlib.import_module(f"config.settings.{_name}")
    for _attr in dir(_module):
        if _attr.isupper():
            globals()[_attr] = getattr(_module, _attr)

_DJANGO_ENV = os.environ.get("DJANGO_ENV", "dev").lower()
if _DJANGO_ENV not in {"dev", "staging", "prod"}:
    raise RuntimeError(f"DJANGO_ENV={_DJANGO_ENV!r} is not valid. Expected one of: dev, staging, prod.")

_env_overrides: ModuleType | None
try:
    _env_overrides = importlib.import_module(f"config.settings.envs.{_DJANGO_ENV}")
except ModuleNotFoundError:
    _env_overrides = None

if _env_overrides is not None:
    for _attr in dir(_env_overrides):
        if not _attr.startswith("_"):
            globals()[_attr] = getattr(_env_overrides, _attr)

# REST_FRAMEWORK/LOGGING sont construits dans les modules de base ; les envs/*.py n'exposent que des deltas, câblés ici.
_throttle_override = globals().get("REST_FRAMEWORK_DEFAULT_THROTTLE_RATES_OVERRIDE")
if _throttle_override:
    globals()["REST_FRAMEWORK"]["DEFAULT_THROTTLE_RATES"].update(_throttle_override)

_root_log_level = globals().get("LOGGING_LEVEL_ROOT")
if _root_log_level:
    globals()["LOGGING"]["root"]["level"] = _root_log_level
