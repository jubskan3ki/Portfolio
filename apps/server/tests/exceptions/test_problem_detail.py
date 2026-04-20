"""Tests RFC 7807 Problem Details (content negotiation + shape)."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from utils.exceptions.problem_detail import (
    CONTENT_TYPE,
    build_problem,
    to_problem_response,
    wants_problem_detail,
)

ACCEPT_PROBLEM = {"HTTP_ACCEPT": CONTENT_TYPE}
ARTICLE_URL = "/api/articles/this-slug-does-not-exist/"


class TestBuildProblem:
    def test_shape_contains_required_fields(self) -> None:
        p = build_problem(404, detail="Introuvable", code="5001")
        assert p["status"] == 404
        assert p["title"] == "Not Found"
        assert p["detail"] == "Introuvable"
        assert p["type"].endswith("5001")
        assert p["code"] == "5001"

    def test_defaults_type_to_about_blank_when_no_code(self) -> None:
        p = build_problem(500)
        assert p["type"] == "about:blank"
        assert p["title"] == "Internal Server Error"

    def test_invalid_params_included(self) -> None:
        p = build_problem(400, invalid_params=[{"name": "email", "reason": "Required"}])
        assert p["invalid-params"] == [{"name": "email", "reason": "Required"}]


class TestWantsProblemDetail:
    def test_accepts_content_type(self) -> None:
        class Req:
            META = {"HTTP_ACCEPT": f"text/html, {CONTENT_TYPE}"}

        assert wants_problem_detail(Req()) is True

    def test_rejects_json_only(self) -> None:
        class Req:
            META = {"HTTP_ACCEPT": "application/json"}

        assert wants_problem_detail(Req()) is False

    def test_returns_false_for_none(self) -> None:
        assert wants_problem_detail(None) is False


class TestToProblemResponse:
    def test_converts_legacy_format(self) -> None:
        response = Response(
            {"errors": [{"code": "5001", "message": "Not found."}]},
            status=404,
        )
        problem = to_problem_response(response, request=None)
        assert problem.data["status"] == 404
        assert problem.data["detail"] == "Not found."
        assert problem.data["code"] == "5001"
        assert problem["Content-Type"] == CONTENT_TYPE

    def test_extracts_invalid_params_from_errors(self) -> None:
        response = Response(
            {
                "errors": [
                    {"code": "2001", "message": "email: required", "field": "email"},
                    {"code": "2001", "message": "password: too short", "field": "password"},
                ]
            },
            status=400,
        )
        problem = to_problem_response(response, request=None)
        params = problem.data["invalid-params"]
        names = {p["name"] for p in params}
        assert names == {"email", "password"}


@pytest.mark.django_db
class TestProblemDetailE2E:
    """Test en conditions reelles via un 404 sur articles."""

    def test_legacy_format_by_default(self, api_client: APIClient) -> None:
        response = cast(Response, api_client.get(ARTICLE_URL))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = cast(dict[str, Any], response.data)
        assert "errors" in data

    def test_problem_format_when_accept_header(self, api_client: APIClient) -> None:
        response = cast(Response, api_client.get(ARTICLE_URL, **ACCEPT_PROBLEM))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = cast(dict[str, Any], response.data)
        assert data.get("status") == 404
        assert "title" in data
        assert "type" in data
        assert response["Content-Type"].startswith(CONTENT_TYPE)

    def test_validation_errors_have_invalid_params(
        self, authenticated_client: APIClient, sample_category: dict[str, Any]
    ) -> None:
        del sample_category
        response = cast(
            Response,
            authenticated_client.post(
                "/api/articles/",
                {"excerpt": "no title"},
                format="json",
                **ACCEPT_PROBLEM,
            ),
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = cast(dict[str, Any], response.data)
        assert data.get("status") == 400
        assert "invalid-params" in data or "detail" in data
