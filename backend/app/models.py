from __future__ import annotations

import datetime as dt
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


# ── Sleep sessions ─────────────────────────────────────────────────────────

class SessionBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    date: dt.date
    bedtime: dt.time
    wake_time: dt.time
    duration_minutes: Annotated[int, Field(ge=0, le=1440)]
    quality_score: Annotated[int, Field(ge=1, le=5)]
    notes: str | None = None


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    date: dt.date | None = None
    bedtime: dt.time | None = None
    wake_time: dt.time | None = None
    duration_minutes: Annotated[int | None, Field(default=None, ge=0, le=1440)]
    quality_score: Annotated[int | None, Field(default=None, ge=1, le=5)]
    notes: str | None = None


class SessionRead(SessionBase):
    id: str
    user_id: str
    created_at: dt.datetime
    updated_at: dt.datetime


# ── Goals ──────────────────────────────────────────────────────────────────

class GoalBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_bedtime: dt.time = dt.time(23, 0)
    target_duration_minutes: Annotated[int, Field(default=480, ge=0, le=1440)]
    weekly_target_nights: Annotated[int, Field(default=7, ge=1, le=7)]


class GoalUpsert(GoalBase):
    pass


class GoalRead(GoalBase):
    user_id: str
    created_at: dt.datetime
    updated_at: dt.datetime


# ── Insights (commit 2) ────────────────────────────────────────────────────

class InsightRead(BaseModel):
    id: str
    user_id: str
    week_start: dt.date
    insight_text: str
    metrics_snapshot: dict
    created_at: dt.datetime
