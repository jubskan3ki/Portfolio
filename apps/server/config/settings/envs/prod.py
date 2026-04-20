"""Production overrides."""

DEBUG = False
ENABLE_DEBUG_TOOLBAR = False

REST_FRAMEWORK_DEFAULT_THROTTLE_RATES_OVERRIDE = {
    "anon": "100/minute",
    "user": "1000/minute",
}

LOGGING_LEVEL_ROOT = "WARNING"
