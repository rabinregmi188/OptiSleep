from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from postgrest import APIError

from ..auth import current_user
from ..db import user_client
from ..models import SessionCreate, SessionRead, SessionUpdate

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


def _serialize_payload(payload: dict) -> dict:
    """Turn `date`/`time` objects into ISO strings for JSON-friendly insert."""
    out = dict(payload)
    if "date" in out and out["date"] is not None:
        out["date"] = out["date"].isoformat()
    for k in ("bedtime", "wake_time"):
        if k in out and out[k] is not None:
            out[k] = out[k].isoformat()
    return out


@router.get("", response_model=list[SessionRead])
def list_sessions(user: Annotated[dict, Depends(current_user)], limit: int = 90):
    db = user_client(user["token"])
    result = (
        db.table("sleep_sessions")
        .select("*")
        .order("date", desc=True)
        .limit(min(limit, 365))
        .execute()
    )
    return result.data


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: SessionCreate,
    user: Annotated[dict, Depends(current_user)],
):
    db = user_client(user["token"])
    row = _serialize_payload(payload.model_dump()) | {"user_id": user["id"]}
    try:
        result = db.table("sleep_sessions").insert(row).execute()
    except APIError as exc:
        if "duplicate key" in str(exc).lower() or getattr(exc, "code", "") == "23505":
            raise HTTPException(status.HTTP_409_CONFLICT, "A session for that date already exists") from exc
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    return result.data[0]


@router.patch("/{session_id}", response_model=SessionRead)
def update_session(
    session_id: str,
    payload: SessionUpdate,
    user: Annotated[dict, Depends(current_user)],
):
    db = user_client(user["token"])
    changes = _serialize_payload(payload.model_dump(exclude_unset=True))
    if not changes:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No fields to update")
    result = db.table("sleep_sessions").update(changes).eq("id", session_id).execute()
    if not result.data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")
    return result.data[0]


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: str, user: Annotated[dict, Depends(current_user)]):
    db = user_client(user["token"])
    result = db.table("sleep_sessions").delete().eq("id", session_id).execute()
    if not result.data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")
    return None
