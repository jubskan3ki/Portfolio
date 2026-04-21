"""Generate OpenAPI schema from drf-spectacular."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()


def generate_schema() -> dict[str, Any]:
    """Generate OpenAPI 3.0 schema using drf-spectacular."""
    from drf_spectacular.generators import SchemaGenerator

    generator = SchemaGenerator(title="Portfolio API", version="1.0.0")
    schema: dict[str, Any] = generator.get_schema(request=None, public=True)
    return schema


def main() -> int:
    """Main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="swagger/openapi.json")
    args = parser.parse_args()

    schema: dict[str, Any] = generate_schema()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False, default=str)

    size = output_path.stat().st_size
    paths_count = len(schema.get("paths", {}))
    print(f"OpenAPI schema saved: {args.output} ({size} bytes, {paths_count} paths)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
