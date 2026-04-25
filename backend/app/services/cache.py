"""Thin Redis JSON cache.

If `REDIS_URL` isn't configured, every method becomes a no-op so the rest of
the API works against a bare Postgres setup. That's the right default for a
portfolio piece — Redis is value-add, not a hard dependency.
"""

from __future__ import annotations

import json
import logging
from functools import lru_cache
from typing import Any

import redis

from ..config import get_settings

log = logging.getLogger(__name__)


class _NoopCache:
    enabled = False

    def get(self, key: str) -> Any | None:
        return None

    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        return None

    def delete(self, key: str) -> None:
        return None


class _RedisCache:
    enabled = True

    def __init__(self, url: str) -> None:
        self._client = redis.from_url(url, decode_responses=True, socket_connect_timeout=2)

    def get(self, key: str) -> Any | None:
        try:
            raw = self._client.get(key)
        except redis.exceptions.RedisError as exc:
            log.warning("redis.get failed (%s); falling back to None", exc)
            return None
        return None if raw is None else json.loads(raw)

    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        try:
            self._client.set(key, json.dumps(value, default=str), ex=ttl_seconds)
        except redis.exceptions.RedisError as exc:
            log.warning("redis.set failed (%s); ignoring", exc)

    def delete(self, key: str) -> None:
        try:
            self._client.delete(key)
        except redis.exceptions.RedisError as exc:
            log.warning("redis.delete failed (%s); ignoring", exc)


@lru_cache
def get_cache() -> _RedisCache | _NoopCache:
    url = get_settings().redis_url
    if not url:
        log.info("REDIS_URL not set — using no-op cache")
        return _NoopCache()
    log.info("Redis cache enabled")
    return _RedisCache(url)
