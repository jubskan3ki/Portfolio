"""`python manage.py migrate_media_to_s3 [--commit]` - copie MEDIA_ROOT vers MinIO."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db.models import FileField, Model


@dataclass(frozen=True)
class MediaField:
    app_label: str
    model_name: str
    field_name: str

    @property
    def qualified(self) -> str:
        return f"{self.app_label}.{self.model_name}.{self.field_name}"


MEDIA_FIELDS: list[MediaField] = [
    MediaField("user", "User", "avatar"),
    MediaField("articles", "Article", "image"),
    MediaField("projects", "Project", "image"),
    MediaField("experiences", "Experience", "logo"),
    MediaField("stacks", "Stack", "logo"),
    MediaField("transfer", "ExportJob", "file"),
]


@dataclass
class Stats:
    uploaded: int = 0
    skipped_already_present: int = 0
    skipped_orphan: int = 0
    failed: int = 0


class Command(BaseCommand):
    help = "Copie les fichiers media du filesystem vers le bucket S3/MinIO (idempotent)."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Effectue reellement les uploads. Sans ce flag, dry-run uniquement.",
        )
        parser.add_argument(
            "--media-root",
            default=None,
            help="Override de MEDIA_ROOT source (par defaut settings.MEDIA_ROOT).",
        )

    def handle(self, *_args, **options) -> None:
        commit: bool = options["commit"]
        media_root = Path(options["media_root"] or settings.MEDIA_ROOT).resolve()

        if not getattr(settings, "USE_S3", False):
            raise CommandError("USE_S3=false : le storage par defaut est FileSystem. Active USE_S3=true et relance.")
        if not media_root.exists():
            raise CommandError(f"MEDIA_ROOT introuvable : {media_root}")

        # Source = filesystem (pas le storage par defaut qui est deja S3).
        fs_storage = FileSystemStorage(location=str(media_root), base_url=settings.MEDIA_URL)

        prefix = "[DRY-RUN] " if not commit else ""
        self.stdout.write(self.style.NOTICE(f"{prefix}Source : {media_root}"))
        self.stdout.write(
            self.style.NOTICE(
                f"{prefix}Cible  : {default_storage.__class__.__module__}.{default_storage.__class__.__name__}"
            )
        )

        stats = Stats()
        for ref in MEDIA_FIELDS:
            self._migrate_field(ref, fs_storage, stats, commit=commit)

        self._print_summary(stats, commit=commit)

    def _migrate_field(
        self,
        ref: MediaField,
        fs_storage: FileSystemStorage,
        stats: Stats,
        *,
        commit: bool,
    ) -> None:
        try:
            model: type[Model] = apps.get_model(ref.app_label, ref.model_name)
        except LookupError:
            self.stderr.write(self.style.WARNING(f"  ? modele introuvable : {ref.qualified}"))
            return

        field = model._meta.get_field(ref.field_name)
        if not isinstance(field, FileField):
            self.stderr.write(self.style.WARNING(f"  ? pas un FileField : {ref.qualified}"))
            return

        qs = model._default_manager.exclude(**{f"{ref.field_name}__isnull": True}).exclude(**{f"{ref.field_name}": ""})
        total = qs.count()
        self.stdout.write(self.style.HTTP_INFO(f"\n{ref.qualified}  ({total} instance(s))"))

        for obj in qs.iterator():
            file_field = getattr(obj, ref.field_name)
            name = file_field.name
            if not name:
                continue
            self._migrate_single_file(name, fs_storage, stats, commit=commit)

    def _migrate_single_file(
        self,
        name: str,
        fs_storage: FileSystemStorage,
        stats: Stats,
        *,
        commit: bool,
    ) -> None:
        if default_storage.exists(name):
            stats.skipped_already_present += 1
            self.stdout.write(f"  = {name} (deja sur S3)")
            return

        local_path = Path(fs_storage.path(name))
        if not local_path.exists():
            stats.skipped_orphan += 1
            self.stderr.write(self.style.WARNING(f"  o orphelin : {name} (en DB, absent du FS)"))
            return

        if not commit:
            stats.uploaded += 1
            self.stdout.write(f"  + {name} ({local_path.stat().st_size} B)")
            return

        try:
            with local_path.open("rb") as src:
                default_storage.save(name, src)
        except OSError as exc:
            stats.failed += 1
            self.stderr.write(self.style.ERROR(f"  x FAIL {name} : {exc}"))
            return
        stats.uploaded += 1
        self.stdout.write(self.style.SUCCESS(f"  + {name}"))

    def _print_summary(self, stats: Stats, *, commit: bool) -> None:
        self.stdout.write("\n" + "=" * 60)
        verb = "Upload" if commit else "Upload (dry-run)"
        self.stdout.write(f"  {verb:.<40} {stats.uploaded:>5}")
        self.stdout.write(f"  Skip (deja sur S3){'.':.<22} {stats.skipped_already_present:>5}")
        self.stdout.write(f"  Skip (orphelin FS){'.':.<22} {stats.skipped_orphan:>5}")
        self.stdout.write(f"  Echec{'.':.<35} {stats.failed:>5}")
        if not commit:
            self.stdout.write(self.style.WARNING("\nDry-run : ajoute --commit pour appliquer."))
        elif stats.failed:
            self.stdout.write(self.style.ERROR("\nMigration partielle, voir erreurs ci-dessus."))
        else:
            self.stdout.write(self.style.SUCCESS("\nMigration OK."))
