#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_TTL_SECONDS = {
    "search": 3600,
    "user": 86400,
    "url": 86400,
}


@dataclass(frozen=True)
class CacheLookup:
    hit: bool
    payload: Optional[Dict[str, Any]]
    path: Path


class ApifyCache:
    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = self._ensure_writable_cache_dir(cache_dir)

    @staticmethod
    def _ensure_writable_cache_dir(cache_dir: Path) -> Path:
        target = cache_dir.expanduser()
        try:
            target.mkdir(parents=True, exist_ok=True)
            probe = target / ".write-test"
            with probe.open("w", encoding="utf-8") as handle:
                handle.write("ok")
            probe.unlink(missing_ok=True)
            return target
        except OSError:
            fallback = Path(tempfile.gettempdir()) / "openclaw-x-apify-cache"
            fallback.mkdir(parents=True, exist_ok=True)
            print(
                f"[cache] Using fallback cache directory: {fallback}",
                file=sys.stderr,
            )
            return fallback

    @staticmethod
    def _make_key(mode: str, query: str, max_results: int) -> str:
        raw = json.dumps(
            {"mode": mode, "query": query, "max_results": max_results},
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _entry_path(self, mode: str, query: str, max_results: int) -> Path:
        key = self._make_key(mode=mode, query=query, max_results=max_results)
        return self.cache_dir / f"{mode}-{key}.json"

    def get(self, mode: str, query: str, max_results: int) -> CacheLookup:
        path = self._entry_path(mode=mode, query=query, max_results=max_results)
        if not path.exists():
            return CacheLookup(hit=False, payload=None, path=path)

        try:
            with path.open("r", encoding="utf-8") as handle:
                cached = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return CacheLookup(hit=False, payload=None, path=path)

        if not isinstance(cached, dict):
            return CacheLookup(hit=False, payload=None, path=path)

        expires_at = cached.get("expires_at")
        payload = cached.get("payload")
        now = int(time.time())

        if not isinstance(expires_at, int) or expires_at <= now:
            return CacheLookup(hit=False, payload=None, path=path)

        if not isinstance(payload, dict):
            return CacheLookup(hit=False, payload=None, path=path)

        return CacheLookup(hit=True, payload=payload, path=path)

    def set(self, mode: str, query: str, max_results: int, payload: Dict[str, Any]) -> None:
        ttl_seconds = DEFAULT_TTL_SECONDS.get(mode, DEFAULT_TTL_SECONDS["search"])
        now = int(time.time())
        entry = {
            "mode": mode,
            "query": query,
            "max_results": max_results,
            "created_at": now,
            "expires_at": now + ttl_seconds,
            "payload": payload,
        }

        path = self._entry_path(mode=mode, query=query, max_results=max_results)
        tmp_path = path.with_suffix(".tmp")

        with tmp_path.open("w", encoding="utf-8") as handle:
            json.dump(entry, handle, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)

    def stats(self) -> Dict[str, int]:
        total_size = 0
        entries = 0
        valid = 0
        expired = 0
        now = int(time.time())

        for path in self.cache_dir.glob("*.json"):
            if not path.is_file():
                continue
            entries += 1
            total_size += path.stat().st_size
            try:
                with path.open("r", encoding="utf-8") as handle:
                    cached = json.load(handle)
                expires_at = cached.get("expires_at")
                if isinstance(expires_at, int) and expires_at > now:
                    valid += 1
                else:
                    expired += 1
            except (OSError, json.JSONDecodeError):
                expired += 1

        return {
            "entries": entries,
            "valid_entries": valid,
            "expired_entries": expired,
            "total_bytes": total_size,
        }

    def clear(self) -> int:
        removed = 0
        for path in self.cache_dir.glob("*.json"):
            try:
                path.unlink(missing_ok=True)
                removed += 1
            except OSError:
                continue
        return removed
