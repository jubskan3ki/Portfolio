"""Dev overrides.

DEBUG/ENABLE_DEBUG_TOOLBAR sont figés dans base.py à partir de DJANGO_ENV.
"""

REST_FRAMEWORK_DEFAULT_THROTTLE_RATES_OVERRIDE = {
    "anon": "1000/minute",
    "user": "5000/minute",
}

LOGGING_LEVEL_ROOT = "DEBUG"
