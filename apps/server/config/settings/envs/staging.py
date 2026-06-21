"""Staging overrides.

DEBUG/ENABLE_DEBUG_TOOLBAR sont figés dans base.py à partir de DJANGO_ENV.
"""

# Laxer than prod for nightly k6 benchmarks.
REST_FRAMEWORK_DEFAULT_THROTTLE_RATES_OVERRIDE = {
    "anon": "500/minute",
    "user": "2000/minute",
}

LOGGING_LEVEL_ROOT = "INFO"
