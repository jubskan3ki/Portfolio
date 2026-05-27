"""Django settings dispatcher. Loads modular settings, then DJANGO_ENV overrides."""

import importlib
import os

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

try:
    _env_overrides = importlib.import_module(f"config.settings.envs.{_DJANGO_ENV}")
except ModuleNotFoundError:
    _env_overrides = None

if _env_overrides is not None:
    for _attr in dir(_env_overrides):
        if not _attr.startswith("_"):
            globals()[_attr] = getattr(_env_overrides, _attr)
