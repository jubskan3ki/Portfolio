"""Dev overrides."""

DEBUG = True
ENABLE_DEBUG_TOOLBAR = True

REST_FRAMEWORK_DEFAULT_THROTTLE_RATES_OVERRIDE = {
    "anon": "1000/minute",
    "user": "5000/minute",
}

LOGGING_LEVEL_ROOT = "DEBUG"
