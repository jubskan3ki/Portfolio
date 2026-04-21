"""Refuse destructive pending migrations before a deploy swap.

Exit codes:
  0 | no pending migrations (safe to deploy).
  1 | pending but non-destructive (apply normally).
  2 | pending and destructive (block deploy, require manual approval).
"""

import ast
import sys
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor

DESTRUCTIVE_OPS = {
    "RemoveField",
    "DeleteModel",
    "RenameField",
    "RenameModel",
    "AlterField",
}


class Command(BaseCommand):
    """Pre-deploy migration safety gate."""

    help = "Inspect pending migrations and refuse destructive operations."

    def handle(self, *_args, **_options):
        connection = connections[DEFAULT_DB_ALIAS]
        executor = MigrationExecutor(connection)
        targets = executor.loader.graph.leaf_nodes()
        plan = executor.migration_plan(targets)
        pending = [(m.app_label, m.name) for m, backwards in plan if not backwards]

        if not pending:
            self.stdout.write(self.style.SUCCESS("no pending migrations"))
            sys.exit(0)

        destructive = []
        for app_label, migration_name in pending:
            path = self._migration_path(app_label, migration_name)
            if path is None:
                continue
            destructive.extend(
                (app_label, migration_name, op) for op in self._extract_operations(path) if op in DESTRUCTIVE_OPS
            )

        for app, name in pending:
            self.stdout.write(f"pending: {app}.{name}")

        if destructive:
            self.stdout.write("")
            self.stdout.write(self.style.ERROR("destructive operations detected:"))
            for app, name, op in destructive:
                self.stdout.write(self.style.ERROR(f"  {app}.{name}: {op}"))
            self.stdout.write(
                self.style.ERROR(
                    "Refusing auto-deploy. Run migrations manually after review "
                    "(make backend-migrate) or split into non-destructive steps."
                )
            )
            sys.exit(2)

        self.stdout.write(self.style.WARNING(f"{len(pending)} non-destructive migrations pending"))
        sys.exit(1)

    def _migration_path(self, app_label: str, migration_name: str) -> Path | None:
        try:
            app_config = apps.get_app_config(app_label)
        except LookupError:
            return None
        candidate = Path(app_config.path) / "migrations" / f"{migration_name}.py"
        return candidate if candidate.is_file() else None

    def _extract_operations(self, path: Path) -> list[str]:
        ops: list[str] = []
        try:
            tree = ast.parse(path.read_text())
        except (OSError, SyntaxError):
            return ops
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Name)
                        and target.id == "operations"
                        and isinstance(node.value, ast.List | ast.Tuple)
                    ):
                        ops.extend(self._operation_name(element) for element in node.value.elts)
        return [o for o in ops if o]

    def _operation_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute):
                return func.attr
            if isinstance(func, ast.Name):
                return func.id
        return ""
