"""
Django management command for code linting.

Usage:
    python manage.py lint               # Check all (ruff check + format check)
    python manage.py lint --fix         # Auto-fix issues
    python manage.py lint --format      # Format code with ruff
    python manage.py lint --mypy        # Also run mypy type checking
    python manage.py lint --black       # Check Black formatting
    python manage.py lint --isort       # Check isort import ordering
    python manage.py lint --flake8      # Run Flake8 linting
    python manage.py lint --all         # Run everything (ruff + black + isort + flake8 + mypy)
"""

import subprocess
import sys
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


def find_tool_in_venvs(tool: str) -> str | None:
    """Find a tool executable in any venv up the directory tree."""
    ext = ".exe" if sys.platform == "win32" else ""
    base = Path(__file__).resolve().parent

    # Search up the directory tree for .venv or venv containing the tool
    for _ in range(10):
        for venv_name in [".venv", "venv"]:
            venv_path = base / venv_name
            if venv_path.exists():
                scripts = venv_path / ("Scripts" if sys.platform == "win32" else "bin")
                tool_path = scripts / f"{tool}{ext}"
                if tool_path.exists():
                    return str(tool_path)
        base = base.parent
    return None


class Command(BaseCommand):
    help = "Run code linting tools (ruff, black, isort, flake8, mypy)"

    def add_arguments(self, parser):
        parser.add_argument("--fix", action="store_true", help="Auto-fix linting issues")
        parser.add_argument("--format", action="store_true", help="Format code with ruff")
        parser.add_argument("--mypy", action="store_true", help="Run mypy type checking")
        parser.add_argument("--black", action="store_true", help="Check Black formatting")
        parser.add_argument("--isort", action="store_true", help="Check isort import ordering")
        parser.add_argument("--flake8", action="store_true", help="Run Flake8 linting")
        parser.add_argument("--all", action="store_true", help="Run all checks including mypy")
        parser.add_argument("paths", nargs="*", default=["."], help="Paths to lint (default: .)")

    def run_tool(self, cmd: list[str], cwd: Path) -> int:
        """Run a tool and return exit code."""
        result = subprocess.run(cmd, cwd=cwd, check=False)
        return result.returncode

    def get_tool_path(self, tool: str) -> str:
        """Get the path to a tool executable."""
        path = find_tool_in_venvs(tool)
        return path if path else tool

    def _tool_available(self, tool: str) -> bool:
        """Check if a tool is installed."""
        path = find_tool_in_venvs(tool)
        if path:
            return True
        result = subprocess.run(
            [tool, "--version"],
            capture_output=True,
            check=False,
        )
        return result.returncode == 0

    def handle(self, *_args, **options):
        base_dir = settings.BASE_DIR
        paths = options["paths"]
        errors = []
        ruff = self.get_tool_path("ruff")

        self.stdout.write(self.style.HTTP_INFO("=" * 60))
        self.stdout.write(self.style.HTTP_INFO(" Code Quality Check"))
        self.stdout.write(self.style.HTTP_INFO("=" * 60 + "\n"))

        # ── Ruff check ──
        self.stdout.write(self.style.MIGRATE_HEADING(">>> Ruff Linter"))
        fix_flag = ["--fix"] if options["fix"] else []
        if self.run_tool([ruff, "check", *fix_flag, *paths], base_dir) != 0:
            errors.append("ruff")
            self.stdout.write(self.style.ERROR("    Issues found\n"))
        else:
            self.stdout.write(self.style.SUCCESS("    OK\n"))

        # ── Ruff format ──
        self.stdout.write(self.style.MIGRATE_HEADING(">>> Ruff Formatter"))
        if options["format"]:
            if self.run_tool([ruff, "format", *paths], base_dir) != 0:
                errors.append("format")
                self.stdout.write(self.style.ERROR("    Failed\n"))
            else:
                self.stdout.write(self.style.SUCCESS("    Done\n"))
        elif self.run_tool([ruff, "format", "--check", *paths], base_dir) != 0:
            errors.append("format")
            self.stdout.write(self.style.WARNING("    Files need formatting (use --format)\n"))
        else:
            self.stdout.write(self.style.SUCCESS("    OK\n"))

        # ── Black ──
        if options["black"] or options["all"]:
            self.stdout.write(self.style.MIGRATE_HEADING(">>> Black Formatter"))
            if not self._tool_available("black"):
                self.stdout.write(self.style.WARNING("    Not installed (pip install black)\n"))
            else:
                black = self.get_tool_path("black")
                if options["fix"]:
                    code = self.run_tool([black, *paths], base_dir)
                else:
                    code = self.run_tool([black, "--check", "--diff", *paths], base_dir)
                if code != 0:
                    errors.append("black")
                    self.stdout.write(self.style.ERROR("    Formatting issues found\n"))
                else:
                    self.stdout.write(self.style.SUCCESS("    OK\n"))

        # ── isort ──
        if options["isort"] or options["all"]:
            self.stdout.write(self.style.MIGRATE_HEADING(">>> isort Import Sorter"))
            if not self._tool_available("isort"):
                self.stdout.write(self.style.WARNING("    Not installed (pip install isort)\n"))
            else:
                isort = self.get_tool_path("isort")
                if options["fix"]:
                    code = self.run_tool([isort, *paths], base_dir)
                else:
                    code = self.run_tool([isort, "--check-only", "--diff", *paths], base_dir)
                if code != 0:
                    errors.append("isort")
                    self.stdout.write(self.style.ERROR("    Import ordering issues found\n"))
                else:
                    self.stdout.write(self.style.SUCCESS("    OK\n"))

        # ── Flake8 ──
        if options["flake8"] or options["all"]:
            self.stdout.write(self.style.MIGRATE_HEADING(">>> Flake8 Linter"))
            if not self._tool_available("flake8"):
                self.stdout.write(self.style.WARNING("    Not installed (pip install flake8)\n"))
            else:
                flake8 = self.get_tool_path("flake8")
                if self.run_tool([flake8, *paths], base_dir) != 0:
                    errors.append("flake8")
                    self.stdout.write(self.style.ERROR("    Issues found\n"))
                else:
                    self.stdout.write(self.style.SUCCESS("    OK\n"))

        # ── MyPy ──
        if options["mypy"] or options["all"]:
            self.stdout.write(self.style.MIGRATE_HEADING(">>> MyPy Type Checker"))
            mypy = self.get_tool_path("mypy")
            python_exe = sys.executable
            if self.run_tool([mypy, "--python-executable", python_exe, *paths], base_dir) != 0:
                errors.append("mypy")
                self.stdout.write(self.style.ERROR("    Type errors found\n"))
            else:
                self.stdout.write(self.style.SUCCESS("    OK\n"))

        # ── Django check ──
        self.stdout.write(self.style.MIGRATE_HEADING(">>> Django System Check"))
        try:
            call_command("check", verbosity=0)
            self.stdout.write(self.style.SUCCESS("    OK\n"))
        except CommandError as e:
            errors.append("django")
            self.stdout.write(self.style.ERROR(f"    {e}\n"))

        # ── Summary ──
        self.stdout.write(self.style.HTTP_INFO("=" * 60))
        if not errors:
            self.stdout.write(self.style.SUCCESS(" All checks passed!"))
        else:
            self.stdout.write(self.style.ERROR(f" Failed: {', '.join(errors)}"))
        self.stdout.write(self.style.HTTP_INFO("=" * 60))

        sys.exit(1 if errors else 0)
