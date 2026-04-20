"""Gestionnaires d'exceptions DRF — format legacy {errors: [...]} + RFC 7807 si Accept le demande."""

import logging
from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from django.http import Http404
from rest_framework import status
from rest_framework import status as http_status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.response import Response

from .error_codes import (
    AUTH_INVALID_CREDENTIALS,
    AUTH_PERMISSION_DENIED,
    RATE_LIMIT_EXCEEDED,
    SERVER_DATABASE_ERROR,
    SERVER_INTERNAL_ERROR,
    SERVER_THIRD_PARTY_ERROR,
    VALIDATION_ALREADY_EXISTS,
    VALIDATION_INVALID_FORMAT,
    VALIDATION_NOT_FOUND,
    format_validation_errors,
)
from .service import ServiceError

logger = logging.getLogger("django.request")


def custom_exception_handler(exc, context):
    """Convertit en RFC 7807 si Accept=application/problem+json, sinon format legacy {errors}."""
    from rest_framework.views import exception_handler as drf_exception_handler

    from .problem_detail import to_problem_response, wants_problem_detail

    response = drf_exception_handler(exc, context)

    if response is None:
        from . import APIError  # import ici pour eviter les imports circulaires

        if isinstance(exc, APIError):
            response = handle_api_error(exc)
        elif isinstance(exc, ServiceError):
            response = handle_service_error(exc)
        elif isinstance(exc, DjangoValidationError):
            response = handle_django_validation_error(exc)
        elif isinstance(exc, IntegrityError):
            response = handle_database_error(exc)
        elif isinstance(exc, Http404):
            response = handle_not_found_error()
        else:
            response = handle_generic_error(exc)
    else:
        response = standardize_response_format(response, exc)

    request = context.get("request") if context else None
    if wants_problem_detail(request):
        response = to_problem_response(response, request)

    return response


def handle_api_error(exc):
    error_data = {
        "code": exc.code or SERVER_INTERNAL_ERROR["code"],
        "message": exc.detail,
    }
    return Response({"errors": [error_data]}, status=exc.status_code)


def handle_service_error(exc: ServiceError) -> Response:
    """Mappe ServiceError -> status HTTP + error code."""
    from .service import (
        ConflictError,
        ExternalServiceError,
        NotFoundError,
        PermissionDeniedError,
        RateLimitError,
    )
    from .service import ValidationError as ServiceValidationError

    status_mapping = {
        NotFoundError: (http_status.HTTP_404_NOT_FOUND, VALIDATION_NOT_FOUND["code"]),
        ServiceValidationError: (http_status.HTTP_400_BAD_REQUEST, VALIDATION_INVALID_FORMAT["code"]),
        PermissionDeniedError: (http_status.HTTP_403_FORBIDDEN, AUTH_PERMISSION_DENIED["code"]),
        ConflictError: (http_status.HTTP_409_CONFLICT, VALIDATION_ALREADY_EXISTS["code"]),
        RateLimitError: (http_status.HTTP_429_TOO_MANY_REQUESTS, RATE_LIMIT_EXCEEDED["code"]),
        ExternalServiceError: (http_status.HTTP_502_BAD_GATEWAY, SERVER_THIRD_PARTY_ERROR["code"]),
    }

    http_status_code: int = http_status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = exc.code

    for error_class, (status_code, code) in status_mapping.items():
        if isinstance(exc, error_class):
            http_status_code = status_code
            if not error_code:
                error_code = code
            break

    error_data: dict[str, Any] = {
        "code": error_code or SERVER_INTERNAL_ERROR["code"],
        "message": exc.message,
    }

    if exc.details:
        error_data["details"] = exc.details

    logger.warning("Service error: %s - %s", error_code, exc.message)

    return Response({"errors": [error_data]}, status=http_status_code)


def handle_django_validation_error(exc):
    if hasattr(exc, "message_dict"):
        errors = format_validation_errors(exc.message_dict)
    else:
        errors = [{"code": VALIDATION_INVALID_FORMAT["code"], "message": str(exc)}]

    return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)


def handle_database_error(exc):
    logger.error("Database error: %s", str(exc), exc_info=True)

    error = SERVER_DATABASE_ERROR.copy()
    if "unique constraint" in str(exc).lower():
        error["message"] = "Cette ressource existe déjà."

    return Response({"errors": [error]}, status=status.HTTP_400_BAD_REQUEST)


def handle_not_found_error():
    return Response({"errors": [VALIDATION_NOT_FOUND]}, status=status.HTTP_404_NOT_FOUND)


def handle_generic_error(exc):
    logger.error("Unhandled exception: %s", str(exc), exc_info=True)

    return Response({"errors": [SERVER_INTERNAL_ERROR]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def standardize_response_format(response, exc):
    """Convertit reponse DRF erreur en format legacy {errors: [...]}."""
    errors = []

    if isinstance(exc, ValidationError):
        errors = format_drf_validation_errors(response.data)
    elif isinstance(exc, NotAuthenticated | AuthenticationFailed):
        errors = [AUTH_INVALID_CREDENTIALS]
    elif isinstance(exc, PermissionDenied):
        errors = [AUTH_PERMISSION_DENIED]
    elif isinstance(exc, NotFound):
        errors = [VALIDATION_NOT_FOUND]
    elif isinstance(exc, APIException):
        errors = [{"code": SERVER_INTERNAL_ERROR["code"], "message": str(exc.detail)}]
    else:
        errors = [{"code": SERVER_INTERNAL_ERROR["code"], "message": str(response.data)}]

    response.data = {"errors": errors}
    return response


def format_drf_validation_errors(validation_data) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    validation_code = VALIDATION_INVALID_FORMAT["code"]

    if isinstance(validation_data, dict):
        for field, error_detail in validation_data.items():
            if isinstance(error_detail, list):
                errors.extend(
                    {
                        "code": validation_code,
                        "message": f"{field}: {error}",
                        "field": field,
                    }
                    for error in error_detail
                )
            else:
                errors.append(
                    {
                        "code": validation_code,
                        "message": f"{field}: {error_detail}",
                        "field": field,
                    }
                )
    elif isinstance(validation_data, list):
        errors.extend({"code": validation_code, "message": str(error)} for error in validation_data)
    else:
        errors.append({"code": validation_code, "message": str(validation_data)})

    return errors
