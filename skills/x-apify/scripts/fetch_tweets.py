#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

from cache import ApifyCache
from config import ApifyConfig, load_config


class ApifyError(RuntimeError):
    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _request_json(
    *,
    method: str,
    url: str,
    timeout: int,
    payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url=url, method=method, headers=headers, data=data)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", errors="replace")
        message = body.strip() or err.reason
        try:
            decoded = json.loads(body)
            # Apify typically returns { error: { message: "..." } }
            if isinstance(decoded, dict):
                error_obj = decoded.get("error")
                if isinstance(error_obj, dict) and isinstance(error_obj.get("message"), str):
                    message = error_obj["message"]
        except json.JSONDecodeError:
            pass
        raise ApifyError(err.code, f"Apify HTTP {err.code}: {message}") from err
    except urllib.error.URLError as err:
        raise RuntimeError(f"Network error while contacting Apify: {err.reason}") from err


def _request_json_list(*, url: str, timeout: int) -> List[Dict[str, Any]]:
    req = urllib.request.Request(url=url, method="GET", headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            payload = json.loads(raw) if raw else []
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", errors="replace")
        raise ApifyError(err.code, f"Apify HTTP {err.code}: {body.strip() or err.reason}") from err
    except urllib.error.URLError as err:
        raise RuntimeError(f"Network error while contacting Apify: {err.reason}") from err

    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        # Some actors can return wrapped payloads.
        maybe_items = payload.get("items")
        if isinstance(maybe_items, list):
            return [item for item in maybe_items if isinstance(item, dict)]
    return []


def _build_actor_input(mode: str, query: str, max_results: int) -> Dict[str, Any]:
    base: Dict[str, Any] = {
        "maxItems": max_results,
        "onlyImage": False,
        "onlyQuote": False,
        "onlyVerifiedUsers": False,
        "sort": "Latest",
    }

    if mode == "search":
        base["searchTerms"] = [query]
    elif mode == "user":
        handles = [part.strip().lstrip("@") for part in query.split(",") if part.strip()]
        base["twitterHandles"] = handles
    elif mode == "url":
        base["tweetUrls"] = [query]
        base["startUrls"] = [query]
    else:
        raise RuntimeError(f"Unsupported mode: {mode}")

    return base


def _run_actor(config: ApifyConfig, actor_input: Dict[str, Any]) -> str:
    actor_id = urllib.parse.quote(config.actor_id, safe="")
    query = urllib.parse.urlencode({"token": config.token, "waitForFinish": "180"})
    run_url = f"{config.base_url}/v2/acts/{actor_id}/runs?{query}"

    run_payload = _request_json(
        method="POST",
        url=run_url,
        timeout=config.timeout_seconds,
        payload=actor_input,
    )
    data = run_payload.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("Unexpected Apify response: missing run data.")

    dataset_id = data.get("defaultDatasetId")
    if not isinstance(dataset_id, str) or not dataset_id:
        raise RuntimeError("Unexpected Apify response: missing defaultDatasetId.")
    return dataset_id


def _fetch_dataset_items(config: ApifyConfig, dataset_id: str, max_results: int) -> List[Dict[str, Any]]:
    query = urllib.parse.urlencode(
        {
            "token": config.token,
            "clean": "true",
            "format": "json",
            "limit": str(max_results),
        }
    )
    items_url = f"{config.base_url}/v2/datasets/{dataset_id}/items?{query}"
    return _request_json_list(url=items_url, timeout=config.timeout_seconds)


def _first_non_empty(values: Iterable[Any]) -> Optional[Any]:
    for value in values:
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        return value
    return None


def _dig(obj: Any, *path: str) -> Any:
    current = obj
    for key in path:
        if not isinstance(current, dict):
            return None
        if key not in current:
            return None
        current = current[key]
    return current


def _as_int(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        try:
            return int(float(value))
        except ValueError:
            return 0
    return 0


def _normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    tweet_id = _first_non_empty(
        (
            item.get("id"),
            item.get("id_str"),
            item.get("tweetId"),
            _dig(item, "tweet", "id"),
            _dig(item, "tweet", "id_str"),
        )
    )
    text = _first_non_empty((item.get("full_text"), item.get("text"), _dig(item, "tweet", "text"))) or ""
    author = _first_non_empty(
        (
            item.get("author"),
            item.get("authorUsername"),
            _dig(item, "author", "userName"),
            _dig(item, "author", "username"),
            _dig(item, "user", "screen_name"),
        )
    )
    author_name = _first_non_empty(
        (
            item.get("authorName"),
            _dig(item, "author", "name"),
            _dig(item, "user", "name"),
        )
    )
    created_at = _first_non_empty(
        (
            item.get("created_at"),
            item.get("createdAt"),
            item.get("timestamp"),
            _dig(item, "tweet", "created_at"),
        )
    )
    url = _first_non_empty((item.get("url"), item.get("tweetUrl")))
    if not url and isinstance(tweet_id, (str, int)) and isinstance(author, str):
        url = f"https://x.com/{author}/status/{tweet_id}"

    likes = _as_int(
        _first_non_empty(
            (
                item.get("likes"),
                item.get("likeCount"),
                item.get("favorite_count"),
                _dig(item, "public_metrics", "like_count"),
            )
        )
    )
    retweets = _as_int(
        _first_non_empty(
            (
                item.get("retweets"),
                item.get("retweetCount"),
                item.get("retweet_count"),
                _dig(item, "public_metrics", "retweet_count"),
            )
        )
    )
    replies = _as_int(
        _first_non_empty(
            (
                item.get("replies"),
                item.get("replyCount"),
                item.get("reply_count"),
                _dig(item, "public_metrics", "reply_count"),
            )
        )
    )

    return {
        "id": str(tweet_id) if tweet_id is not None else "",
        "text": str(text),
        "author": str(author) if author is not None else "",
        "author_name": str(author_name) if author_name is not None else "",
        "created_at": str(created_at) if created_at is not None else "",
        "likes": likes,
        "retweets": retweets,
        "replies": replies,
        "url": str(url) if url is not None else "",
    }


def fetch_tweets(config: ApifyConfig, mode: str, query: str, max_results: int) -> Dict[str, Any]:
    actor_input = _build_actor_input(mode=mode, query=query, max_results=max_results)
    dataset_id = _run_actor(config=config, actor_input=actor_input)
    raw_items = _fetch_dataset_items(config=config, dataset_id=dataset_id, max_results=max_results)
    tweets = [_normalize_item(item) for item in raw_items]

    payload = {
        "query": query,
        "mode": mode,
        "fetched_at": utc_now_iso(),
        "count": len(tweets),
        "tweets": tweets,
    }
    return payload


def render_summary(payload: Dict[str, Any]) -> str:
    mode_label = {
        "search": "Search",
        "user": "User",
        "url": "Tweet URL",
    }.get(str(payload.get("mode")), "Result")

    fetched_at = str(payload.get("fetched_at", ""))
    tweets = payload.get("tweets", [])
    if not isinstance(tweets, list):
        tweets = []

    lines = [
        f"=== X/Twitter {mode_label} Results ===",
        f"Query: {payload.get('query', '')}",
        f"Fetched: {fetched_at}",
        f"Results: {len(tweets)} tweets",
        "",
    ]

    for item in tweets:
        if not isinstance(item, dict):
            continue
        lines.extend(
            [
                "---",
                f"@{item.get('author', '')} ({item.get('author_name', '')})",
                str(item.get("created_at", "")),
                str(item.get("text", "")),
                (
                    f"[Likes: {item.get('likes', 0)} | "
                    f"RTs: {item.get('retweets', 0)} | "
                    f"Replies: {item.get('replies', 0)}]"
                ),
                str(item.get("url", "")),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch X/Twitter data via Apify.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--search", help="Search query text or hashtags.")
    mode.add_argument("--user", help="Twitter handles (single or comma-separated).")
    mode.add_argument("--url", help="Specific tweet URL.")

    parser.add_argument("--max-results", type=int, default=20, help="Maximum number of results.")
    parser.add_argument("--format", choices=["json", "summary"], default="json", help="Output format.")
    parser.add_argument("--output", help="Output file path.")
    parser.add_argument("--no-cache", action="store_true", help="Bypass cache and fetch fresh data.")
    parser.add_argument("--cache-stats", action="store_true", help="Show cache stats and exit.")
    parser.add_argument("--clear-cache", action="store_true", help="Clear cache and exit.")
    return parser.parse_args()


def print_or_write(output: str, output_path: Optional[str]) -> None:
    if output_path:
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(output)
        print(output_path)
        return
    print(output)


def main() -> int:
    args = parse_args()
    config = load_config()
    cache = ApifyCache(config.cache_dir)

    if args.cache_stats:
        stats = cache.stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return 0

    if args.clear_cache:
        removed = cache.clear()
        print(f"Cleared cache entries: {removed}")
        return 0

    if not config.token:
        eprint("Error: APIFY_API_TOKEN is required.")
        eprint("Set it with: export APIFY_API_TOKEN='apify_api_...'\n")
        return 1

    mode: Optional[str] = None
    query: Optional[str] = None

    if args.search:
        mode = "search"
        query = args.search.strip()
    elif args.user:
        mode = "user"
        query = args.user.strip()
    elif args.url:
        mode = "url"
        query = args.url.strip()

    if not mode or not query:
        eprint("Error: one of --search, --user, or --url is required.")
        return 1

    max_results = max(1, int(args.max_results))

    payload: Optional[Dict[str, Any]] = None
    if not args.no_cache:
        lookup = cache.get(mode=mode, query=query, max_results=max_results)
        if lookup.hit and lookup.payload is not None:
            payload = lookup.payload
            eprint(f"[cached] Results for: {query}")

    if payload is None:
        try:
            payload = fetch_tweets(config=config, mode=mode, query=query, max_results=max_results)
        except ApifyError as err:
            message = str(err)
            if err.status == 401:
                eprint("Error: invalid APIFY_API_TOKEN.")
            elif err.status in (402, 429):
                eprint("Error: Apify quota/rate limit reached.")
            else:
                eprint("Error while calling Apify.")
            eprint(message)
            return 1
        except Exception as err:
            eprint(f"Error: {err}")
            return 1

        if not args.no_cache:
            cache.set(mode=mode, query=query, max_results=max_results, payload=payload)

    if args.format == "summary":
        output_text = render_summary(payload)
    else:
        output_text = json.dumps(payload, ensure_ascii=False, indent=2)

    try:
        print_or_write(output_text, args.output)
    except OSError as err:
        eprint(f"Error writing output: {err}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
