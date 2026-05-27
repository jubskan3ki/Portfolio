"""Storage backend. USE_S3=true active S3Storage (MinIO self-hosted) ; sinon FileSystemStorage."""

import copy
from typing import cast

import environ

from config.settings import base as _base

_env = environ.Env(USE_S3=(bool, False))

USE_S3: bool = cast(bool, _env.bool("USE_S3", default=False))

MEDIA_URL = "/media/"

if USE_S3:
    AWS_S3_ENDPOINT_URL = _env("S3_ENDPOINT_URL", default="http://minio:9000")
    AWS_ACCESS_KEY_ID = _env("S3_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = _env("S3_SECRET_KEY")
    AWS_STORAGE_BUCKET_NAME = _env("S3_BUCKET_NAME", default="portfolio-media")
    AWS_S3_REGION_NAME = _env("S3_REGION", default="us-east-1")
    AWS_S3_ADDRESSING_STYLE = _env("S3_ADDRESSING_STYLE", default="path")
    AWS_S3_SIGNATURE_VERSION = "s3v4"

    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "public, max-age=31536000, immutable"}

    AWS_S3_CUSTOM_DOMAIN = _env("S3_PUBLIC_DOMAIN", default="localhost:9000/portfolio-media")
    AWS_S3_URL_PROTOCOL = _env("S3_PUBLIC_PROTOCOL", default="http") + ":"
    AWS_S3_VERIFY = _env.bool("S3_VERIFY_SSL", default=False)

    STORAGES = copy.deepcopy(_base.STORAGES)
    STORAGES["default"] = {"BACKEND": "storages.backends.s3.S3Storage"}
    MEDIA_URL = f"{AWS_S3_URL_PROTOCOL}//{AWS_S3_CUSTOM_DOMAIN}/"
