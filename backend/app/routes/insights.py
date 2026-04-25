"""Weekly LLM-generated insight.

Resolution order on a request:
  1. Redis cache (1h TTL)
  2. `insights` table (this week's row)
  3. Compute summary → call Gemini → write to table → cache → return.

Step 3 is the only one that costs a Gemini call, and only the first request
per user per week takes that path.
"""

from __future__ import annotations

import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..auth import current_user
from ..db import service_client, user_client
from ..services.analytics import compute_summary, week_start
from ..services.cache import get_cache
from ..services.gemini import GeminiUnavailable, generate_weekly_insight

router = APIRouter(prefix="/api/insights", tags=["insights"])


class WeeklyInsight(BaseModel):
    week_start: dt.date
    insight_text: str
    metrics_snapshot: dict
    cached: bool = False


@router.get("/weekly", response_model=WeeklyInsight)
def get_weekly_insight(user: Annotated[dict, Depends(current_user)]):
    today = dt.date.today()
    monday = week_start(today)
    cache = get_cache()
    cache_key = f"insight:{user['id']}:{monday.isoformat()}"

    # 1. hot cache
    if (hit := cache.get(cache_key)) is not None:
        return WeeklyInsight(**hit, cached=True)

    db = user_client(user["token"])

    # 2. persisted row for the week
    existing = (
        db.table("insights")
        .select("*")
        .eq("user_id", user["id"])
        .eq("week_start", monday.isoformat())
        .maybe_single()
        .execute()
    )
    if existing and existing.data:
        payload = {
            "week_start": existing.data["week_start"],
            "insight_text": existing.data["insight_text"],
            "metrics_snapshot": existing.data["metrics_snapshot"],
        }
        cache.set(cache_key, payload, ttl_seconds=3600)
        return WeeklyInsight(**payload, cached=True)

    # 3. compute → Gemini → persist
    sessions = (
        db.table("sleep_sessions")
        .select("*")
        .order("date", desc=True)
        .limit(14)
        .execute()
        .data
        or []
    )
    if not sessions:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Log at least one sleep session before requesting an insight.",
        )

    goal_resp = db.table("goals").select("*").eq("user_id", user["id"]).maybe_single().execute()
    goal = goal_resp.data if goal_resp else None

    summary = compute_summary(sessions, goal, today=today)

    try:
        text = generate_weekly_insight(summary, goal)
    except GeminiUnavailable as exc:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            f"Coaching service unavailable: {exc}",
        ) from exc

    # Persist with the service role so we don't depend on the user's RLS policies
    # for the write path.
    service_client().table("insights").insert(
        {
            "user_id": user["id"],
            "week_start": monday.isoformat(),
            "insight_text": text,
            "metrics_snapshot": summary,
        }
    ).execute()

    payload = {
        "week_start": monday.isoformat(),
        "insight_text": text,
        "metrics_snapshot": summary,
    }
    cache.set(cache_key, payload, ttl_seconds=3600)
    return WeeklyInsight(**payload, cached=False)
