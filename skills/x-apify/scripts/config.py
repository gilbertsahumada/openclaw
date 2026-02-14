#!/usr/bin/env python3
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


DEFAULT_ACTOR_ID = "quacker/twitter-scraper"
DEFAULT_BASE_URL = "https://api.apify.com"
DEFAULT_TIMEOUT_SECONDS = 120


@dataclass(frozen=True)
class ApifyConfig:
    token: str
    actor_id: str
    base_url: str
    timeout_seconds: int
    cache_dir: Path


def _resolve_skill_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def _resolve_default_cache_dir() -> Path:
    xdg_cache_home = os.getenv("XDG_CACHE_HOME", "").strip()
    if xdg_cache_home:
        return Path(xdg_cache_home).expanduser() / "openclaw" / "x-apify"
    return Path.home() / ".cache" / "openclaw" / "x-apify"


def load_config() -> ApifyConfig:
    token = os.getenv("APIFY_API_TOKEN", "").strip()
    actor_id = os.getenv("APIFY_ACTOR_ID", DEFAULT_ACTOR_ID).strip() or DEFAULT_ACTOR_ID
    base_url = os.getenv("APIFY_BASE_URL", DEFAULT_BASE_URL).strip() or DEFAULT_BASE_URL
    timeout_raw = os.getenv("APIFY_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS)).strip()

    timeout_seconds = DEFAULT_TIMEOUT_SECONDS
    try:
        parsed = int(timeout_raw)
        if parsed > 0:
            timeout_seconds = parsed
    except (TypeError, ValueError):
        timeout_seconds = DEFAULT_TIMEOUT_SECONDS

    cache_dir_raw = os.getenv("X_APIFY_CACHE_DIR", "").strip()
    cache_dir = Path(cache_dir_raw).expanduser() if cache_dir_raw else _resolve_default_cache_dir()

    return ApifyConfig(
        token=token,
        actor_id=actor_id,
        base_url=base_url.rstrip("/"),
        timeout_seconds=timeout_seconds,
        cache_dir=cache_dir,
    )
