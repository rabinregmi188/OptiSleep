"""Pure functions that turn a list of sleep_session rows into metrics.

No I/O here — easy to unit-test, and the same code powers both the
`/api/analytics/summary` endpoint and the Gemini prompt builder.
"""

from __future__ import annotations

import datetime as dt
from statistics import mean, pstdev
from typing import Any


# ── time helpers ────────────────────────────────────────────────────────────

def _bedtime_minutes_from_noon(time_str: str) -> int:
    """Map a bedtime string ("HH:MM" or "HH:MM:SS") onto minutes-since-noon.

    Why noon? It avoids the midnight wrap that would treat 11:55pm and 12:05am
    as 24 hours apart. With a noon origin, 22:00 → 600, 00:00 → 720, 02:00 → 840.
    """
    parts = time_str.split(":")
    hour, minute = int(parts[0]), int(parts[1])
    return ((hour - 12) % 24) * 60 + minute


def _minutes_from_noon_to_clock(minutes: int) -> str:
    minutes = int(round(minutes)) % (24 * 60)
    hour = (minutes // 60 + 12) % 24
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"


# ── streak ──────────────────────────────────────────────────────────────────

def _current_streak(dates: list[dt.date], today: dt.date | None = None) -> int:
    """Consecutive nights ending today or yesterday.

    Yesterday counts as the streak's tail too — users may not have logged
    today yet by the time they open the app.
    """
    if not dates:
        return 0
    today = today or dt.date.today()
    sorted_desc = sorted(set(dates), reverse=True)
    if sorted_desc[0] not in (today, today - dt.timedelta(days=1)):
        return 0
    streak = 0
    expected = sorted_desc[0]
    for d in sorted_desc:
        if d == expected:
            streak += 1
            expected = expected - dt.timedelta(days=1)
        else:
            break
    return streak


# ── summary ─────────────────────────────────────────────────────────────────

EMPTY_SUMMARY: dict[str, Any] = {
    "sleep_score": 0,
    "sessions_count": 0,
    "avg_duration_minutes": 0,
    "avg_quality": 0.0,
    "avg_bedtime": None,
    "weekend_drift_minutes": 0,
    "bedtime_consistency_minutes": 0,
    "current_streak": 0,
}


def compute_summary(
    sessions: list[dict],
    goal: dict | None = None,
    *,
    today: dt.date | None = None,
) -> dict[str, Any]:
    """Aggregate metrics over the given sessions.

    Sessions are dicts (rows from PostgREST) with at minimum:
    `date` (str), `bedtime` (str), `duration_minutes` (int), `quality_score` (int).
    """
    if not sessions:
        return EMPTY_SUMMARY.copy()

    target_minutes = int((goal or {}).get("target_duration_minutes") or 480)

    durations = [int(s["duration_minutes"]) for s in sessions]
    qualities = [int(s["quality_score"]) for s in sessions]
    bedtimes_min = [_bedtime_minutes_from_noon(str(s["bedtime"])) for s in sessions]
    dates = [
        s["date"] if isinstance(s["date"], dt.date) else dt.date.fromisoformat(str(s["date"]))
        for s in sessions
    ]

    avg_duration = mean(durations)
    avg_quality = mean(qualities)
    avg_bedtime_min = mean(bedtimes_min)

    weekday_bt = [bt for bt, d in zip(bedtimes_min, dates) if d.weekday() < 5]
    weekend_bt = [bt for bt, d in zip(bedtimes_min, dates) if d.weekday() >= 5]
    weekend_drift = (mean(weekend_bt) - mean(weekday_bt)) if weekday_bt and weekend_bt else 0.0

    consistency = pstdev(bedtimes_min) if len(bedtimes_min) >= 2 else 0.0

    duration_score = min(100.0, (avg_duration / target_minutes) * 100)
    quality_score = ((avg_quality - 1) / 4) * 100  # 1..5 → 0..100
    consistency_score = max(0.0, 100.0 - (consistency / 60.0) * 100.0)
    sleep_score = round(0.5 * duration_score + 0.3 * quality_score + 0.2 * consistency_score)

    return {
        "sleep_score": int(sleep_score),
        "sessions_count": len(sessions),
        "avg_duration_minutes": round(avg_duration),
        "avg_quality": round(avg_quality, 1),
        "avg_bedtime": _minutes_from_noon_to_clock(avg_bedtime_min),
        "weekend_drift_minutes": round(weekend_drift),
        "bedtime_consistency_minutes": round(consistency),
        "current_streak": _current_streak(dates, today=today),
    }


def week_start(today: dt.date | None = None) -> dt.date:
    today = today or dt.date.today()
    return today - dt.timedelta(days=today.weekday())  # Monday
