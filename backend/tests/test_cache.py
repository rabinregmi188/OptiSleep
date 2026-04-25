"""The cache layer should silently no-op when REDIS_URL is unset."""

from app.services.cache import _NoopCache, get_cache


def test_noop_cache_returns_none_on_get():
    c = _NoopCache()
    assert c.get("anything") is None


def test_noop_cache_set_and_delete_dont_raise():
    c = _NoopCache()
    c.set("k", {"a": 1}, ttl_seconds=10)
    c.delete("k")  # smoke


def test_default_cache_is_noop_when_redis_url_missing(monkeypatch):
    # conftest sets minimal env without REDIS_URL, so the cache should be no-op
    monkeypatch.delenv("REDIS_URL", raising=False)
    get_cache.cache_clear()
    cache = get_cache()
    assert isinstance(cache, _NoopCache)
    assert cache.enabled is False
