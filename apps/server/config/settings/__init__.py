"""Django settings dispatcher. DJANGO_ENV=dev|staging|prod loads envs/*.py overrides."""

import importlib
import os
from types import ModuleType

_BASE_MODULES = (
    "config.settings.base",
    "config.settings.cache",
    "config.settings.celery_conf",
    "config.settings.database",
    "config.settings.email",
    "config.settings.jwt",
    "config.settings.logging_conf",
    "config.settings.rest_framework",
    "config.settings.security",
)

for _mod_name in _BASE_MODULES:
    _mod = importlib.import_module(_mod_name)
    for _name in dir(_mod):
        if not _name.startswith("_") and _name.isupper():
            globals()[_name] = getattr(_mod, _name)

_DJANGO_ENV = os.environ.get("DJANGO_ENV", "dev").lower()
if _DJANGO_ENV not in {"dev", "staging", "prod"}:
    raise RuntimeError(f"DJANGO_ENV={_DJANGO_ENV!r} is not valid. Expected one of: dev, staging, prod.")

_env_overrides: ModuleType | None
try:
    _env_overrides = importlib.import_module(f"config.settings.envs.{_DJANGO_ENV}")
except ModuleNotFoundError:
    _env_overrides = None

if _env_overrides is not None:
    for _name in dir(_env_overrides):
        if not _name.startswith("_"):
            globals()[_name] = getattr(_env_overrides, _name)
