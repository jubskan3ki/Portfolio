"""Tests PR #5 : HMAC + timestamp + backoff exponentiel."""

from __future__ import annotations

import pytest

from core.webhooks.services.dispatcher import (
    BACKOFF_BASE_SECONDS,
    BACKOFF_MAX_SECONDS,
    compute_backoff_delay,
)

from ..factories import AdminFactory, UserFactory, WebhookFactory


@pytest.mark.django_db
class TestHmacSignature:
    """HMAC-SHA256 : signing + verification en temps constant."""

    def test_signature_deterministic_for_same_input(self) -> None:
        webhook = WebhookFactory(created_by=AdminFactory())
        s1 = webhook.generate_signature("hello world")
        s2 = webhook.generate_signature("hello world")
        assert s1 == s2
        assert len(s1) == 64

    def test_signature_changes_with_payload(self) -> None:
        webhook = WebhookFactory(created_by=AdminFactory())
        assert webhook.generate_signature("a") != webhook.generate_signature("b")

    def test_signature_changes_with_timestamp(self) -> None:
        webhook = WebhookFactory(created_by=AdminFactory())
        assert webhook.generate_signature("payload", "100") != webhook.generate_signature("payload", "200")

    def test_verify_signature_accepts_valid(self) -> None:
        webhook = WebhookFactory(created_by=AdminFactory())
        sig = webhook.generate_signature("payload", "1700000000")
        assert webhook.verify_signature("payload", sig, "1700000000") is True

    def test_verify_signature_rejects_tampered_payload(self) -> None:
        webhook = WebhookFactory(created_by=AdminFactory())
        sig = webhook.generate_signature("payload", "1700000000")
        assert webhook.verify_signature("tampered", sig, "1700000000") is False

    def test_verify_signature_rejects_tampered_timestamp(self) -> None:
        webhook = WebhookFactory(created_by=AdminFactory())
        sig = webhook.generate_signature("payload", "1700000000")
        assert webhook.verify_signature("payload", sig, "1700000001") is False

    def test_verify_signature_rejects_wrong_signature(self) -> None:
        webhook = WebhookFactory(created_by=AdminFactory())
        assert webhook.verify_signature("payload", "deadbeef" * 8, "1700000000") is False

    def test_different_webhooks_produce_different_signatures(self) -> None:
        w1 = WebhookFactory(created_by=UserFactory())
        w2 = WebhookFactory(created_by=UserFactory())
        assert w1.generate_signature("payload") != w2.generate_signature("payload")


class TestExponentialBackoff:
    """compute_backoff_delay : true exponential + cap + jitter."""

    def test_attempt_0_or_negative_returns_base(self) -> None:
        assert compute_backoff_delay(0) == BACKOFF_BASE_SECONDS
        assert compute_backoff_delay(-5) == BACKOFF_BASE_SECONDS

    def test_grows_exponentially(self) -> None:
        # Avec jitter de 20%, attempt=2 doit toujours etre > attempt=1 en esperance
        # on compare avec une marge : min(2) >= max(1 with jitter)
        # attempt 1 : ~30s +/- 6 -> [24, 36]
        # attempt 2 : ~60s +/- 12 -> [48, 72]
        # Les plages ne se chevauchent pas.
        samples_1 = [compute_backoff_delay(1) for _ in range(50)]
        samples_2 = [compute_backoff_delay(2) for _ in range(50)]
        assert max(samples_1) < min(samples_2)

    def test_capped_at_max(self) -> None:
        for _ in range(20):
            assert compute_backoff_delay(20) <= int(BACKOFF_MAX_SECONDS * 1.2) + 1

    def test_jitter_produces_variability(self) -> None:
        samples = {compute_backoff_delay(3) for _ in range(30)}
        assert len(samples) > 1

    def test_delay_is_positive(self) -> None:
        for attempt in range(1, 15):
            assert compute_backoff_delay(attempt) > 0
