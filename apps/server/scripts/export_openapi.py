"""Generate OpenAPI schema from drf-yasg."""

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

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


def get_fallback_schema() -> dict[str, Any]:
    """Return minimal fallback schema."""
    return {
        "swagger": "2.0",
        "info": {
            "title": "Portfolio API",
            "description": "API pour le portfolio personnel",
            "version": "v1",
        },
        "host": "localhost:8000",
        "schemes": ["http", "https"],
        "basePath": "/api",
        "paths": {},
        "definitions": {},
    }


def make_serializable(obj: Any) -> dict[str, Any] | list[Any] | Any:
    """Convert object to JSON-serializable format."""
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items() if not k.startswith("_")}
    if isinstance(obj, (list, tuple)):
        return [make_serializable(item) for item in obj]
    if hasattr(obj, "as_odict"):
        return make_serializable(obj.as_odict())
    if hasattr(obj, "__dict__"):
        return make_serializable(obj.__dict__)
    try:
        json.dumps(obj)
        return obj
    except (TypeError, OverflowError):
        return str(obj)


def generate_schema() -> dict[str, Any]:
    """Generate OpenAPI schema."""
    info = openapi.Info(
        title="Portfolio API",
        default_version="v1",
        description="API pour le portfolio personnel",
        contact=openapi.Contact(email=settings.ADMIN_EMAIL),
        license=openapi.License(name="BSD License"),
    )

    try:
        generator = OpenAPISchemaGenerator(info=info)
        schema = generator.get_schema(request=None, public=True)
        result = make_serializable(schema)

        if not isinstance(result, dict):
            return get_fallback_schema()

        schema_dict: dict[str, Any] = result

        if "swagger" not in schema_dict and "openapi" not in schema_dict:
            schema_dict["swagger"] = "2.0"

        return schema_dict

    except (ImportError, AttributeError, ValueError, TypeError) as e:
        print(f"Warning: {e}")
        return get_fallback_schema()


def main() -> int:
    """Main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="swagger/openapi.json")
    args = parser.parse_args()

    schema: dict[str, Any] = generate_schema()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    size = output_path.stat().st_size
    paths_dict = schema.get("paths", {})
    paths_count = len(paths_dict) if isinstance(paths_dict, dict) else 0
    print(f"OpenAPI schema saved: {args.output} ({size} bytes, {paths_count} paths)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
