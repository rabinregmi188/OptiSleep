"""Supabase client wrappers.

Two flavors:
- `user_client(token)` — talks to PostgREST as the end user, so RLS policies apply.
- `service_client()` — bypasses RLS for backend-only writes (insights, scheduled jobs).
"""

from functools import lru_cache

from supabase import Client, create_client

from .config import get_settings


@lru_cache
def service_client() -> Client:
    s = get_settings()
    return create_client(s.supabase_url, s.supabase_service_role_key)


def user_client(access_token: str) -> Client:
    """Per-request client. The user's JWT is forwarded so RLS policies fire."""
    s = get_settings()
    client = create_client(s.supabase_url, s.supabase_anon_key)
    client.postgrest.auth(access_token)
    return client
