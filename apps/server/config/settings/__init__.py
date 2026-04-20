"""Django settings dispatcher. DJANGO_ENV=dev|staging|prod loads envs/*.py overrides."""

import importlib
import os

from config.settings.base import *  # noqa: F403
from config.settings.cache import *  # noqa: F403
from config.settings.celery_conf import *  # noqa: F403
from config.settings.database import *  # noqa: F403
from config.settings.email import *  # noqa: F403
from config.settings.jwt import *  # noqa: F403
from config.settings.logging_conf import *  # noqa: F403
from config.settings.rest_framework import *  # noqa: F403
from config.settings.security import *  # noqa: F403

_DJANGO_ENV = os.environ.get("DJANGO_ENV", "dev").lower()
if _DJANGO_ENV not in {"dev", "staging", "prod"}:
    raise RuntimeError(f"DJANGO_ENV={_DJANGO_ENV!r} is not valid. Expected one of: dev, staging, prod.")

try:
    _env_overrides = importlib.import_module(f"config.settings.envs.{_DJANGO_ENV}")
except ModuleNotFoundError:
    _env_overrides = None

if _env_overrides is not None:
    for _name in dir(_env_overrides):
        if not _name.startswith("_"):
            globals()[_name] = getattr(_env_overrides, _name)
