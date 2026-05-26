"""Rollup quotidien des Web Vitals : agrege puis purge les vieux events.

Affiche par metrique (sur la fenetre demandee) : count, mean, p75, p95 et la
distribution des ratings. Optionnellement purge les events anterieurs a la
fenetre de retention pour garder la table compacte.

Usage typique (cron quotidien) :
    python manage.py aggregate_web_vitals --days 7 --retention-days 30
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from datetime import timedelta
from statistics import fmean
from typing import Any, TypedDict

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from core.stats.models import WebVitalEvent

logger = logging.getLogger("core.stats")

RATINGS = ("good", "needs-improvement", "poor")


class _MetricSummary(TypedDict):
    metric_name: str
    count: int
    mean: float
    p75: float | None
    p95: float | None
    ratings: dict[str, int]


def _percentile(values: list[float], percentile: int) -> float | None:
    if not values:
        return None
    sorted_values = sorted(values)
    index = round((len(sorted_values) - 1) * (percentile / 100))
    return float(sorted_values[index])


class Command(BaseCommand):
    help = "Aggrege les Web Vitals sur N jours et purge les events anciens."

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument(
            "--days",
            type=int,
            default=1,
            help="Fenetre d'agregation en jours (defaut: 1).",
        )
        parser.add_argument(
            "--retention-days",
            type=int,
            default=None,
            help="Si fourni, supprime les events plus vieux que N jours.",
        )
        parser.add_argument(
            "--json",
            action="store_true",
            help="Sortie au format JSON (sinon: texte lisible).",
        )

    def handle(self, *_args: Any, **options: Any) -> None:
        days = options["days"]
        retention_days = options["retention_days"]
        as_json = options["json"]

        if days < 1:
            raise CommandError("--days doit etre >= 1.")
        if retention_days is not None and retention_days < days:
            raise CommandError("--retention-days doit etre >= --days.")

        since = timezone.now() - timedelta(days=days)
        events = list(WebVitalEvent.objects.filter(created_at__gte=since).values("metric_name", "value", "rating"))

        values_by_metric: dict[str, list[float]] = defaultdict(list)
        ratings_by_metric: dict[str, dict[str, int]] = defaultdict(lambda: dict.fromkeys(RATINGS, 0))
        for event in events:
            metric_name = str(event["metric_name"])
            values_by_metric[metric_name].append(float(event["value"]))
            rating = str(event["rating"])
            if rating in ratings_by_metric[metric_name]:
                ratings_by_metric[metric_name][rating] += 1

        metrics_summary: list[_MetricSummary] = []
        for metric_name in sorted(values_by_metric.keys()):
            values = values_by_metric[metric_name]
            metrics_summary.append(
                {
                    "metric_name": metric_name,
                    "count": len(values),
                    "mean": round(float(fmean(values)), 2),
                    "p75": _percentile(values, 75),
                    "p95": _percentile(values, 95),
                    "ratings": ratings_by_metric[metric_name],
                }
            )

        purged = 0
        if retention_days is not None:
            cutoff = timezone.now() - timedelta(days=retention_days)
            purged, _ = WebVitalEvent.objects.filter(created_at__lt=cutoff).delete()

        payload = {
            "window_days": days,
            "total_events": len(events),
            "purged": purged,
            "retention_days": retention_days,
            "metrics": metrics_summary,
        }

        logger.info(
            "aggregate_web_vitals window=%dd events=%d purged=%d",
            days,
            len(events),
            purged,
        )

        if as_json:
            self.stdout.write(json.dumps(payload, indent=2, sort_keys=True))
            return

        self.stdout.write(self.style.SUCCESS(f"Web Vitals rollup ({days}d) : {len(events)} events, {purged} purged"))
        if not metrics_summary:
            self.stdout.write("  (aucune metrique)")
            return

        for metric in metrics_summary:
            ratings = metric["ratings"]
            self.stdout.write(
                "  {name:<5} count={count:<6} mean={mean:<10} p75={p75} p95={p95}  "
                "good={good} needs={needs} poor={poor}".format(
                    name=metric["metric_name"],
                    count=metric["count"],
                    mean=metric["mean"],
                    p75=metric["p75"],
                    p95=metric["p95"],
                    good=ratings["good"],
                    needs=ratings["needs-improvement"],
                    poor=ratings["poor"],
                )
            )
