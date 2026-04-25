import datetime as dt

from app.services.analytics import (
    EMPTY_SUMMARY,
    _bedtime_minutes_from_noon,
    _current_streak,
    _minutes_from_noon_to_clock,
    compute_summary,
    week_start,
)


def _session(day: dt.date, *, bedtime: str, duration: int, quality: int = 4) -> dict:
    return {
        "date": day.isoformat(),
        "bedtime": bedtime,
        "wake_time": "07:00",
        "duration_minutes": duration,
        "quality_score": quality,
    }


# ── time helpers ────────────────────────────────────────────────────────────

def test_bedtime_minutes_handles_late_night():
    assert _bedtime_minutes_from_noon("22:00") == 600
    assert _bedtime_minutes_from_noon("23:30") == 690
    assert _bedtime_minutes_from_noon("00:00") == 720
    assert _bedtime_minutes_from_noon("02:00") == 840


def test_bedtime_minutes_round_trip():
    for clock in ("19:00", "22:30", "00:15", "03:45"):
        rt = _minutes_from_noon_to_clock(_bedtime_minutes_from_noon(clock))
        assert rt == clock


# ── streak ──────────────────────────────────────────────────────────────────

def test_streak_includes_today_and_yesterday():
    today = dt.date(2026, 4, 25)
    dates = [today, today - dt.timedelta(days=1), today - dt.timedelta(days=2)]
    assert _current_streak(dates, today=today) == 3


def test_streak_starts_from_yesterday_if_today_missing():
    today = dt.date(2026, 4, 25)
    dates = [today - dt.timedelta(days=1), today - dt.timedelta(days=2)]
    assert _current_streak(dates, today=today) == 2


def test_streak_breaks_with_gap():
    today = dt.date(2026, 4, 25)
    dates = [today, today - dt.timedelta(days=2)]  # gap on day -1
    assert _current_streak(dates, today=today) == 1


def test_streak_zero_if_neither_today_nor_yesterday():
    today = dt.date(2026, 4, 25)
    dates = [today - dt.timedelta(days=3)]
    assert _current_streak(dates, today=today) == 0


def test_streak_empty_returns_zero():
    assert _current_streak([], today=dt.date(2026, 4, 25)) == 0


# ── summary ─────────────────────────────────────────────────────────────────

def test_summary_empty_returns_zeros():
    out = compute_summary([])
    assert out == EMPTY_SUMMARY


def test_summary_basic_metrics():
    today = dt.date(2026, 4, 25)
    sessions = [
        _session(today - dt.timedelta(days=i), bedtime="23:00", duration=480, quality=4)
        for i in range(7)
    ]
    s = compute_summary(sessions, goal={"target_duration_minutes": 480}, today=today)
    assert s["sessions_count"] == 7
    assert s["avg_duration_minutes"] == 480
    assert s["avg_quality"] == 4.0
    assert s["avg_bedtime"] == "23:00"
    assert s["bedtime_consistency_minutes"] == 0
    assert s["weekend_drift_minutes"] == 0
    assert s["current_streak"] == 7


def test_summary_weekend_drift_positive_when_later_on_weekends():
    # Build a Mon-Sun week: weekdays at 23:00, Sat+Sun at 01:00 (next day)
    today = dt.date(2026, 4, 26)  # Sunday
    monday = today - dt.timedelta(days=6)
    sessions = []
    for i in range(7):
        d = monday + dt.timedelta(days=i)
        bt = "01:00" if d.weekday() >= 5 else "23:00"
        sessions.append(_session(d, bedtime=bt, duration=480, quality=4))
    s = compute_summary(sessions, goal=None, today=today)
    # Weekend bedtimes are 120 min later than weekday
    assert s["weekend_drift_minutes"] == 120


def test_summary_sleep_score_drops_with_short_duration():
    today = dt.date(2026, 4, 25)
    short = [
        _session(today - dt.timedelta(days=i), bedtime="23:00", duration=300, quality=3)
        for i in range(5)
    ]
    long = [
        _session(today - dt.timedelta(days=i), bedtime="23:00", duration=480, quality=5)
        for i in range(5)
    ]
    s_short = compute_summary(short, goal={"target_duration_minutes": 480}, today=today)
    s_long = compute_summary(long, goal={"target_duration_minutes": 480}, today=today)
    assert s_short["sleep_score"] < s_long["sleep_score"]


def test_summary_consistency_penalty():
    today = dt.date(2026, 4, 25)
    chaotic = []
    for i in range(7):
        bt = "23:00" if i % 2 == 0 else "02:00"  # 3-hour swing each night
        chaotic.append(_session(today - dt.timedelta(days=i), bedtime=bt, duration=480, quality=4))
    s = compute_summary(chaotic, today=today)
    assert s["bedtime_consistency_minutes"] > 60


# ── week_start ──────────────────────────────────────────────────────────────

def test_week_start_returns_monday():
    sun = dt.date(2026, 4, 26)
    assert week_start(sun) == dt.date(2026, 4, 20)
    mon = dt.date(2026, 4, 20)
    assert week_start(mon) == mon
    wed = dt.date(2026, 4, 22)
    assert week_start(wed) == dt.date(2026, 4, 20)
