"""Logging configuration."""

from pathlib import Path

from config.settings.base import BASE_DIR, DEBUG

# LOGGING

LOG_DIR = BASE_DIR / "logs"
try:
    LOG_DIR.mkdir(mode=0o755, exist_ok=True)
except (PermissionError, OSError):
    LOG_DIR = Path("/tmp")

DJANGO_LOG_FILE: Path | None = None
_log_file_path = LOG_DIR / "django_errors.log"
try:
    _log_file_path.touch(mode=0o644, exist_ok=True)
    DJANGO_LOG_FILE = _log_file_path
except (PermissionError, OSError):
    pass

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "with_correlation": {
            "format": "{levelname} {asctime} [{correlation_id}] {module} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple" if DEBUG else "verbose",
        },
        "null": {"class": "logging.NullHandler"},
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO" if DEBUG else "ERROR",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "core": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "ERROR",
            "propagate": True,
        },
        "core.audit": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
        "core.cache": {
            "handlers": ["console"],
            "level": "INFO" if DEBUG else "WARNING",
            "propagate": False,
        },
        "core.stats": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "security": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING" if DEBUG else "ERROR",
            "propagate": False,
        },
    },
}

if DJANGO_LOG_FILE:
    handlers = LOGGING.get("handlers", {})
    loggers = LOGGING.get("loggers", {})
    if isinstance(handlers, dict) and isinstance(loggers, dict):
        handlers["file"] = {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(DJANGO_LOG_FILE),
            "formatter": "verbose",
            "maxBytes": 10485760,
            "backupCount": 5,
        }
        for logger_name in ["django", "core", "celery"]:
            logger_config = loggers.get(logger_name)
            if isinstance(logger_config, dict) and "handlers" in logger_config:
                handler_list = logger_config["handlers"]
                if isinstance(handler_list, list):
                    handler_list.append("file")
