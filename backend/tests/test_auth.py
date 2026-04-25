from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.auth import current_user
from app.config import get_settings


def _make_token(payload: dict, secret: str) -> str:
    return jwt.encode(payload, secret, algorithm="HS256")


def test_valid_token_returns_user():
    settings = get_settings()
    now = datetime.now(timezone.utc)
    token = _make_token(
        {
            "sub": "user-uuid-123",
            "email": "test@example.com",
            "aud": "authenticated",
            "exp": int((now + timedelta(hours=1)).timestamp()),
        },
        settings.supabase_jwt_secret,
    )
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    user = current_user(credentials=creds, settings=settings)
    assert user["id"] == "user-uuid-123"
    assert user["email"] == "test@example.com"


def test_missing_token_raises_401():
    with pytest.raises(HTTPException) as exc:
        current_user(credentials=None, settings=get_settings())
    assert exc.value.status_code == 401


def test_expired_token_raises_401():
    settings = get_settings()
    now = datetime.now(timezone.utc)
    token = _make_token(
        {
            "sub": "user-uuid-123",
            "aud": "authenticated",
            "exp": int((now - timedelta(seconds=10)).timestamp()),
        },
        settings.supabase_jwt_secret,
    )
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    with pytest.raises(HTTPException) as exc:
        current_user(credentials=creds, settings=settings)
    assert exc.value.status_code == 401


def test_wrong_secret_raises_401():
    creds = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=_make_token(
            {"sub": "u", "aud": "authenticated", "exp": 9999999999},
            "different-secret",
        ),
    )
    with pytest.raises(HTTPException) as exc:
        current_user(credentials=creds, settings=get_settings())
    assert exc.value.status_code == 401
