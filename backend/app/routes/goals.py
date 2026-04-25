from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..auth import current_user
from ..db import user_client
from ..models import GoalRead, GoalUpsert

router = APIRouter(prefix="/api/goals", tags=["goals"])


def _serialize(payload: dict) -> dict:
    out = dict(payload)
    if "target_bedtime" in out and out["target_bedtime"] is not None:
        out["target_bedtime"] = out["target_bedtime"].isoformat()
    return out


@router.get("", response_model=GoalRead | None)
def get_goal(user: Annotated[dict, Depends(current_user)]):
    db = user_client(user["token"])
    result = db.table("goals").select("*").eq("user_id", user["id"]).maybe_single().execute()
    return result.data


@router.put("", response_model=GoalRead)
def upsert_goal(
    payload: GoalUpsert,
    user: Annotated[dict, Depends(current_user)],
):
    db = user_client(user["token"])
    row = _serialize(payload.model_dump()) | {"user_id": user["id"]}
    result = db.table("goals").upsert(row, on_conflict="user_id").execute()
    if not result.data:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to save goal")
    return result.data[0]
