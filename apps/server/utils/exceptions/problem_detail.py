"""RFC 7807 Problem Details (activation opt-in via Accept: application/problem+json)."""

from __future__ import annotations

from typing import Any

from rest_framework.response import Response

CONTENT_TYPE = "application/problem+json"
PROBLEM_URI_BASE = "https://portfolio.example.com/problems"


TITLES_BY_STATUS: dict[int, str] = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    409: "Conflict",
    415: "Unsupported Media Type",
    422: "Unprocessable Entity",
    429: "Too Many Requests",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
}


def wants_problem_detail(request: Any) -> bool:
    if request is None:
        return False
    accept = request.META.get("HTTP_ACCEPT", "") if hasattr(request, "META") else ""
    return CONTENT_TYPE in accept


def _first_error(data: dict[str, Any]) -> dict[str, Any]:
    errors = data.get("errors") or []
    if errors and isinstance(errors[0], dict):
        return errors[0]
    return {}


def _build_invalid_params(data: dict[str, Any]) -> list[dict[str, Any]]:
    errors = data.get("errors") or []
    return [
        {"name": err["field"], "reason": err.get("message", "")}
        for err in errors
        if isinstance(err, dict) and err.get("field")
    ]


def build_problem(
    status_code: int,
    *,
    detail: str | None = None,
    code: str | None = None,
    instance: str | None = None,
    invalid_params: list[dict[str, Any]] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    title = TITLES_BY_STATUS.get(status_code, "Error")
    problem: dict[str, Any] = {
        "type": f"{PROBLEM_URI_BASE}/{code}" if code else "about:blank",
        "title": title,
        "status": status_code,
    }
    if detail:
        problem["detail"] = detail
    if instance:
        problem["instance"] = instance
    if code:
        problem["code"] = code
    if invalid_params:
        problem["invalid-params"] = invalid_params
    if extra:
        problem.update(extra)
    return problem


def to_problem_response(response: Response, request: Any = None) -> Response:
    """Convertit {errors: [...]} legacy vers RFC 7807."""
    data = response.data if isinstance(response.data, dict) else {}
    first = _first_error(data)
    invalid_params = _build_invalid_params(data)

    problem = build_problem(
        status_code=response.status_code,
        detail=first.get("message"),
        code=str(first.get("code")) if first.get("code") else None,
        instance=getattr(request, "path", None) if request is not None else None,
        invalid_params=invalid_params or None,
    )

    response.data = problem
    response["Content-Type"] = CONTENT_TYPE
    return response
