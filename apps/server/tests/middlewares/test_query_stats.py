"""Tests du middleware QueryStatsMiddleware (PR #7 perf DB)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from django.http import HttpResponse
from django.test import override_settings

from middlewares.query_stats import N_PLUS_ONE_THRESHOLD, QueryStatsMiddleware, _fingerprint


def _make_request(method: str = "GET", path: str = "/test/"):
    req = MagicMock()
    req.method = method
    req.path = path
    return req


class TestFingerprint:
    def test_numbers_normalised(self) -> None:
        a = _fingerprint("SELECT * FROM articles WHERE id = 1")
        b = _fingerprint("SELECT * FROM articles WHERE id = 42")
        assert a == b

    def test_strings_normalised(self) -> None:
        a = _fingerprint("SELECT * FROM a WHERE slug = 'hello'")
        b = _fingerprint("SELECT * FROM a WHERE slug = 'world'")
        assert a == b

    def test_different_tables_differ(self) -> None:
        a = _fingerprint("SELECT * FROM articles")
        b = _fingerprint("SELECT * FROM projects")
        assert a != b


class TestNPlusOneDetector:
    def test_detects_repeated_pattern(self) -> None:
        sql_template = "SELECT * FROM articles WHERE id = %s"
        queries = [{"sql": sql_template, "time": "0.001"} for _ in range(N_PLUS_ONE_THRESHOLD + 2)]
        result = QueryStatsMiddleware._detect_n_plus_one(queries)
        assert len(result) == 1

    def test_ignores_below_threshold(self) -> None:
        queries = [{"sql": "SELECT 1", "time": "0.001"}] * (N_PLUS_ONE_THRESHOLD - 1)
        assert QueryStatsMiddleware._detect_n_plus_one(queries) == []

    def test_skips_empty_sql(self) -> None:
        queries = [{"sql": "", "time": "0.001"}] * 10
        assert QueryStatsMiddleware._detect_n_plus_one(queries) == []


class TestMiddlewareNoOpWhenDebugOff:
    @override_settings(DEBUG=False)
    def test_not_active_when_debug_off(self) -> None:
        get_response = MagicMock(return_value=HttpResponse("ok"))
        mw = QueryStatsMiddleware(get_response)
        response = mw(_make_request())
        assert "X-Query-Count" not in response
        get_response.assert_called_once()


@pytest.mark.django_db
class TestMiddlewareAddsHeaders:
    """En DEBUG le middleware ajoute les headers de stats DB."""

    @override_settings(DEBUG=True)
    def test_adds_query_count_header(self) -> None:
        from django.contrib.auth import get_user_model

        def get_response(_request):
            get_user_model().objects.count()
            return HttpResponse("ok")

        mw = QueryStatsMiddleware(get_response)
        response = mw(_make_request())
        assert "X-Query-Count" in response
        assert "X-Query-Time-Ms" in response

    @override_settings(DEBUG=True)
    def test_no_n_plus_one_header_when_no_repetition(self) -> None:
        def get_response(_request):
            return HttpResponse("ok")

        mw = QueryStatsMiddleware(get_response)
        response = mw(_make_request())
        assert "X-N-Plus-One" not in response


class TestSuspiciousLogging:
    def test_high_count_triggers_warning(self) -> None:
        with __import__("unittest.mock").mock.patch("middlewares.query_stats.logger") as mock_logger:
            QueryStatsMiddleware._log_if_suspicious(_make_request(), query_count=100, duration_ms=10, n_plus_one=[])
            assert mock_logger.warning.called

    def test_normal_request_no_warning(self) -> None:
        with __import__("unittest.mock").mock.patch("middlewares.query_stats.logger") as mock_logger:
            QueryStatsMiddleware._log_if_suspicious(_make_request(), query_count=2, duration_ms=5, n_plus_one=[])
            assert not mock_logger.warning.called

    def test_n_plus_one_triggers_warning(self) -> None:
        with __import__("unittest.mock").mock.patch("middlewares.query_stats.logger") as mock_logger:
            QueryStatsMiddleware._log_if_suspicious(
                _make_request(), query_count=5, duration_ms=10, n_plus_one=[("SELECT", 10)]
            )
            assert mock_logger.warning.called
