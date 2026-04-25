from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from ..auth import current_user
from ..db import user_client
from ..services.analytics import compute_summary
from ..services.cache import get_cache

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


class SummaryResponse(BaseModel):
    sleep_score: int
    sessions_count: int
    avg_duration_minutes: int
    avg_quality: float
    avg_bedtime: str | None
    weekend_drift_minutes: int
    bedtime_consistency_minutes: int
    current_streak: int


@router.get("/summary", response_model=SummaryResponse)
def get_summary(
    user: Annotated[dict, Depends(current_user)],
    days: int = Query(default=30, ge=1, le=180),
):
    cache = get_cache()
    cache_key = f"analytics:{user['id']}:{days}"

    if (cached := cache.get(cache_key)) is not None:
        return cached

    db = user_client(user["token"])
    sessions = (
        db.table("sleep_sessions").select("*").order("date", desc=True).limit(days).execute().data or []
    )
    goal_resp = db.table("goals").select("*").eq("user_id", user["id"]).maybe_single().execute()
    goal = goal_resp.data if goal_resp else None

    summary = compute_summary(sessions, goal)
    cache.set(cache_key, summary, ttl_seconds=300)  # 5 min — analytics is cheap-ish
    return summary
