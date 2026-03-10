"""Database configuration."""

from config.settings.base import DEBUG, env

# DATABASE
# When using PgBouncer (transaction pooling), CONN_MAX_AGE must be 0
# so Django doesn't hold persistent connections that conflict with pooling.
_USE_PGBOUNCER = env.bool("USE_PGBOUNCER", default=False)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "CONN_MAX_AGE": 0 if (_USE_PGBOUNCER or DEBUG) else 60,
        "OPTIONS": {
            "connect_timeout": 10,
            "client_encoding": "UTF8",
            "sslmode": "prefer" if not DEBUG else "disable",
            "application_name": "django-portfolio",
        },
    }
}
