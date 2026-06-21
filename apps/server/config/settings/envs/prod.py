"""Production overrides.

DEBUG/ENABLE_DEBUG_TOOLBAR ne sont PAS surchargés ici : ils sont figés dans
base.py à partir de DJANGO_ENV, avant les settings qui en dépendent.
"""

REST_FRAMEWORK_DEFAULT_THROTTLE_RATES_OVERRIDE = {
    "anon": "100/minute",
    "user": "1000/minute",
}

LOGGING_LEVEL_ROOT = "WARNING"
