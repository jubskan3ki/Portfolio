"""Container bootstrap: replaces the legacy setup.sh shell script.

Validates env, waits for DB, runs migrations, creates admin, generates OpenAPI
schema, collects static, then execs gunicorn (replacing the current process).

Used as the backend image CMD:
    CMD ["python", "manage.py", "bootstrap"]
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import OperationalError, connections

logger = logging.getLogger("bootstrap")

APP_DIR = Path("/app")
LOG_DIR = APP_DIR / "logs"
SCRIPTS_DIR = APP_DIR / "scripts"
SWAGGER_DIR = APP_DIR / "swagger"

REQUIRED_ENV = (
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "ADMIN_EMAIL",
    "ADMIN_PASSWORD",
)

RUNTIME_DIRS = (
    "logs",
    "media",
    "media/blog",
    "media/projects",
    "media/user",
    "staticfiles",
    "swagger",
    ".cache",
)

DB_WAIT_MAX_ATTEMPTS = 30
DB_WAIT_INTERVAL_SECONDS = 2

MIGRATE_MAX_ATTEMPTS = 5
MIGRATE_RETRY_INTERVAL_SECONDS = 3

MINIMAL_OPENAPI = '{"swagger":"2.0","info":{"title":"Portfolio API","version":"v1"},"paths":{},"definitions":{}}'


class Command(BaseCommand):
    help = "Run pre-flight checks, migrations, collectstatic, then exec gunicorn."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-serve",
            action="store_true",
            help="Run setup only, do not exec gunicorn. Useful for one-shot jobs.",
        )

    def handle(self, *_args, **options):
        start = time.monotonic()
        self._log("INFO", "=== Django bootstrap starting ===")

        self._check_env()
        self._setup_dirs()
        self._wait_for_db()
        self._run_migrations()
        self._create_admin()
        self._generate_openapi()
        self._collect_static()

        self._log("OK", f"bootstrap completed in {time.monotonic() - start:.1f}s")

        if options["no_serve"]:
            return

        self._exec_gunicorn()  # replaces current process, never returns

    def _log(self, level: str, msg: str) -> None:
        line = f"[{time.strftime('%H:%M:%S')}] {level}: {msg}"
        self.stdout.write(line)
        logger.info(msg)

    def _check_env(self) -> None:
        missing = [var for var in REQUIRED_ENV if not os.environ.get(var)]
        if missing:
            raise CommandError(f"Missing env vars: {', '.join(missing)}")
        self._log("OK", "environment variables present")

    def _setup_dirs(self) -> None:
        for sub in RUNTIME_DIRS:
            (APP_DIR / sub).mkdir(parents=True, exist_ok=True)
        self._log("OK", "runtime directories ready")

    def _wait_for_db(self) -> None:
        host, port = self._direct_db_target()
        with self._direct_db_connection():
            for attempt in range(1, DB_WAIT_MAX_ATTEMPTS + 1):
                try:
                    connections["default"].close()
                    with connections["default"].cursor() as cursor:
                        cursor.execute("SELECT 1")
                        cursor.fetchone()
                    self._log("OK", f"database queryable at {host}:{port}")
                    return
                except OperationalError as err:
                    self._log("INFO", f"DB not ready ({attempt}/{DB_WAIT_MAX_ATTEMPTS}): {err.__class__.__name__}")
                    time.sleep(DB_WAIT_INTERVAL_SECONDS)
        raise CommandError(f"database {host}:{port} unreachable after {DB_WAIT_MAX_ATTEMPTS} attempts")

    def _run_migrations(self) -> None:
        self._log("INFO", "running migrations")
        with self._direct_db_connection():
            last_err: Exception | None = None
            for attempt in range(1, MIGRATE_MAX_ATTEMPTS + 1):
                try:
                    call_command("migrate", no_input=True, verbosity=1)
                    self._log("OK", "migrations done")
                    return
                except OperationalError as err:
                    last_err = err
                    self._log("WARN", f"migrate failed ({attempt}/{MIGRATE_MAX_ATTEMPTS}): {err}")
                    connections["default"].close()
                    time.sleep(MIGRATE_RETRY_INTERVAL_SECONDS)
        raise CommandError(f"migrations failed after {MIGRATE_MAX_ATTEMPTS} attempts: {last_err}")

    @staticmethod
    def _direct_db_target() -> tuple[str, str]:
        """Direct (bypass pgbouncer) DB endpoint for bootstrap-time work."""
        host = os.environ.get("DB_HOST_DIRECT") or os.environ["DB_HOST"]
        port = os.environ.get("DB_PORT_DIRECT") or os.environ["DB_PORT"]
        return host, port

    @contextmanager
    def _direct_db_connection(self):
        """Temporarily route Django's default DB connection to the direct endpoint.

        PgBouncer in transaction pooling is fragile for DDL/migrations and adds a
        DNS dependency on the pooler resolving the upstream. Bootstrap-time work
        runs better against the database directly.
        """
        host, port = self._direct_db_target()
        cfg = connections.databases["default"]
        original_host, original_port = cfg["HOST"], cfg["PORT"]
        if (host, port) == (original_host, original_port):
            yield
            return
        connections["default"].close()
        cfg["HOST"] = host
        cfg["PORT"] = port
        self._log("INFO", f"bootstrap using direct DB connection {host}:{port}")
        try:
            yield
        finally:
            connections["default"].close()
            cfg["HOST"] = original_host
            cfg["PORT"] = original_port

    def _create_admin(self) -> None:
        script = SCRIPTS_DIR / "create_admin.py"
        if not script.is_file():
            self._log("WARN", "scripts/create_admin.py missing | skipping admin setup")
            return
        result = subprocess.run([sys.executable, str(script)], check=False)
        if result.returncode == 0:
            self._log("OK", "admin user ready")
        else:
            self._log("WARN", f"create_admin exited with code {result.returncode}")

    def _generate_openapi(self) -> None:
        script = SCRIPTS_DIR / "export_openapi.py"
        output = SWAGGER_DIR / "openapi.json"
        SWAGGER_DIR.mkdir(parents=True, exist_ok=True)
        if script.is_file():
            result = subprocess.run(
                [sys.executable, str(script), "--output", str(output)],
                check=False,
            )
            if result.returncode == 0:
                self._log("OK", f"OpenAPI schema -> {output}")
                return
            self._log("WARN", f"export_openapi failed ({result.returncode}), writing stub")
        output.write_text(MINIMAL_OPENAPI)

    def _collect_static(self) -> None:
        try:
            call_command("collectstatic", no_input=True, clear=True, verbosity=0)
            self._log("OK", "static files collected")
        except Exception as err:
            self._log("WARN", f"collectstatic failed: {err}")

    def _exec_gunicorn(self) -> None:
        workers = os.environ.get("GUNICORN_WORKERS", "3")
        timeout = os.environ.get("GUNICORN_TIMEOUT", "120")
        graceful = os.environ.get("GUNICORN_GRACEFUL_TIMEOUT", "30")
        keep_alive = os.environ.get("GUNICORN_KEEP_ALIVE", "5")

        argv = []
        if os.environ.get("OTEL_ENABLED", "false").lower() == "true":
            if self._which("opentelemetry-instrument"):
                self._log("INFO", f"OTel enabled -> {os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT', 'unset')}")
                argv.append("opentelemetry-instrument")
            else:
                self._log("WARN", "OTEL_ENABLED=true but opentelemetry-instrument not installed")

        argv.extend(
            [
                "gunicorn",
                "config.wsgi:application",
                "--bind",
                "0.0.0.0:8000",
                f"--workers={workers}",
                f"--timeout={timeout}",
                f"--graceful-timeout={graceful}",
                f"--keep-alive={keep_alive}",
                "--worker-tmp-dir=/dev/shm",
                "--log-level=info",
                "--access-logfile=-",
                "--error-logfile=-",
                "--max-requests=1000",
                "--max-requests-jitter=50",
            ]
        )

        self._log("INFO", f"exec {' '.join(argv)}")
        # Bootstrap entrypoint: resolve the binary via PATH, then exec with absolute path.
        resolved = self._which(argv[0])
        if resolved is None:
            raise CommandError(f"Executable not found on PATH: {argv[0]}")
        os.execv(resolved, argv)

    @staticmethod
    def _which(executable: str) -> str | None:
        for path_dir in os.environ.get("PATH", "").split(os.pathsep):
            candidate = Path(path_dir) / executable
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return str(candidate)
        return None
