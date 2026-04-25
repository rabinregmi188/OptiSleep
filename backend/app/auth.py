"""Supabase JWT verification.

The frontend obtains a JWT from Supabase Auth and sends it as a Bearer token.
We verify it with the project's JWT secret (HS256) and pass the user id to
route handlers via the `current_user_id` dependency.
"""

from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import Settings, get_settings

bearer_scheme = HTTPBearer(auto_error=False)


def current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict:
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token")
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token") from exc
    if "sub" not in payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token missing subject")
    return {"id": payload["sub"], "email": payload.get("email"), "token": credentials.credentials}


def current_user_id(user: Annotated[dict, Depends(current_user)]) -> str:
    return user["id"]
