"""One throttled, caching HTTP fetcher for OpenAlex, Crossref and DataCite.

All network access in this project goes through `Fetcher.get_json`, which:
- runs requests strictly one at a time (no threads, no async);
- waits at least `min_interval` seconds between requests;
- backs off exponentially on 429 / 5xx and network errors, honouring Retry-After;
- caches every raw response body under data/raw/ (gzipped for OpenAlex list/search
  responses) so runs are reproducible and resumable.

OpenAlex (Stage 2 onwards): requests carry the personal key from the environment variable
OPENALEX_API_KEY as the `api_key` parameter. The key is never printed, logged, cached or
committed: it is stripped from every URL before it is written anywhere, and responses are
checked for it before they are cached. Every non-cached OpenAlex call is appended to
data/raw/api_ledger.csv with its cost and the remaining daily credits reported by the API
(X-RateLimit-* headers). When the remaining credits fall below RESERVE_CREDITS the fetcher
raises BudgetPaused instead of spending more (free key: 10,000 credits/day; a search costs
10 credits, a filter-only list 1, a single work 0).
"""
from __future__ import annotations

import csv
import datetime as dt
import gzip
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
LEDGER = RAW / "api_ledger.csv"
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"
RESERVE_CREDITS = int(os.environ.get("OPENALEX_RESERVE_CREDITS", "800"))


class BudgetPaused(RuntimeError):
    pass


def _key():
    return os.environ.get("OPENALEX_API_KEY", "")


def redact(s: str) -> str:
    k = _key()
    return s.replace(k, "***") if k else s


def _read_cache(p: Path):
    if p.suffix == ".gz":
        with gzip.open(p, "rt") as f:
            return json.load(f)
    return json.loads(p.read_text())


def _write_cache(p: Path, text: str):
    k = _key()
    if k and k in text:
        raise RuntimeError(f"refusing to cache a response containing the API key: {p.name}")
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix == ".gz":
        with gzip.open(p, "wt", compresslevel=9) as f:
            f.write(text)
    else:
        p.write_text(text)


class Fetcher:
    def __init__(self, min_interval: float = 1.0, max_retries: int = 6, label: str = ""):
        self.min_interval = min_interval
        self.max_retries = max_retries
        self.label = label
        self.session = requests.Session()
        self.session.headers["User-Agent"] = (
            "literature-map/0.2 (research bibliography; mailto:%s)"
            % os.environ.get("OPENALEX_MAILTO", "unset")
        )
        if os.path.exists(CA_BUNDLE):
            self.session.verify = CA_BUNDLE
        self._last = 0.0
        self.network_calls = 0
        self.cache_hits = 0
        self.remaining = None

    def _wait(self):
        dt_ = time.monotonic() - self._last
        if dt_ < self.min_interval:
            time.sleep(self.min_interval - dt_)
        self._last = time.monotonic()

    def _log(self, r, cache_path: Path):
        h = r.headers
        self.remaining = int(h["X-RateLimit-Remaining"]) if h.get("X-RateLimit-Remaining") else None
        new = not LEDGER.exists()
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with LEDGER.open("a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["utc", "label", "status", "cost_usd", "credits_used_today",
                            "credits_remaining", "cache_file"])
            w.writerow([dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                        self.label, r.status_code, h.get("X-RateLimit-Cost-USD", ""),
                        h.get("X-RateLimit-Credits-Used", ""), h.get("X-RateLimit-Remaining", ""),
                        str(cache_path.relative_to(ROOT))])

    def get_json(self, url: str, params: dict | None, cache_path: Path):
        """Return parsed JSON for url, from cache_path if present. None on 404."""
        if cache_path.exists():
            self.cache_hits += 1
            body = _read_cache(cache_path)
            return None if body.get("_status") == 404 else body
        params = dict(params or {})
        is_oa = "openalex.org" in url
        if is_oa:
            if _key():
                params["api_key"] = _key()
            if os.environ.get("OPENALEX_MAILTO"):
                params["mailto"] = os.environ["OPENALEX_MAILTO"]
            if self.remaining is not None and self.remaining < RESERVE_CREDITS:
                raise BudgetPaused(f"OpenAlex credits remaining {self.remaining} < reserve "
                                   f"{RESERVE_CREDITS}; pausing")
        delay = 2.0
        for attempt in range(self.max_retries):
            self._wait()
            self.network_calls += 1
            try:
                r = self.session.get(url, params=params, timeout=90)
            except requests.RequestException as e:
                print(f"  network error {redact(repr(e))[:200]}; retry in {delay:.0f}s",
                      file=sys.stderr)
                time.sleep(delay)
                delay *= 2
                continue
            if is_oa:
                self._log(r, cache_path)
            if r.status_code == 200:
                _write_cache(cache_path, r.text)
                return r.json()
            if r.status_code == 404:
                _write_cache(cache_path, json.dumps({"_status": 404, "url": redact(r.url)}))
                return None
            if r.status_code == 429 or r.status_code >= 500:
                if is_oa and r.status_code == 429 and "X-RateLimit-Remaining" in r.headers \
                        and int(r.headers["X-RateLimit-Remaining"] or 0) <= 0:
                    raise BudgetPaused("OpenAlex daily budget exhausted (HTTP 429)")
                ra = r.headers.get("Retry-After")
                wait = float(ra) if ra and ra.isdigit() and float(ra) < 120 else delay
                if r.status_code == 429 and ra and ra.isdigit() and float(ra) >= 120:
                    raise RuntimeError(f"Rate limited for {ra}s: {redact(r.text[:300])}")
                print(f"  HTTP {r.status_code}; retry in {wait:.0f}s", file=sys.stderr)
                time.sleep(wait)
                delay *= 2
                continue
            raise RuntimeError(f"HTTP {r.status_code} on {redact(r.url)}: {redact(r.text[:300])}")
        raise RuntimeError(f"Gave up after {self.max_retries} attempts: {redact(url)}")

    # ------------------------------------------------------------------ OpenAlex
    def openalex_work(self, wid: str):
        gz = RAW / "works" / f"{wid}.json.gz"
        plain = RAW / "works" / f"{wid}.json"
        return self.get_json(f"https://api.openalex.org/works/{wid}", None,
                             plain if plain.exists() else gz)

    def openalex_list(self, params: dict, cache_name: str):
        """A /works list or search request; the raw response is cached gzipped."""
        return self.get_json("https://api.openalex.org/works", params,
                             RAW / "api" / f"{cache_name}.json.gz")

    # ------------------------------------------------------------------ DOIs
    def crossref_work(self, doi: str):
        safe = doi.replace("/", "_")
        return self.get_json(
            f"https://api.crossref.org/works/{doi}", None, RAW / "crossref" / f"{safe}.json"
        )

    def datacite_work(self, doi: str):
        safe = doi.replace("/", "_")
        return self.get_json(
            f"https://api.datacite.org/dois/{doi}", None, RAW / "datacite" / f"{safe}.json"
        )


_INDEX = None
_FILE_CACHE: dict = {}


def _index():
    """work ID -> cached search response holding that work (data/raw/works_index.json)."""
    global _INDEX
    if _INDEX is None:
        p = RAW / "works_index.json"
        _INDEX = json.loads(p.read_text()) if p.exists() else {}
    return _INDEX


def index_response(cache_rel: str, resp: dict):
    """Record where each work of a search response is cached (the response itself is the
    raw record: works are not stored twice)."""
    idx = _index()
    for w in resp.get("results", []):
        idx.setdefault(w["id"].rsplit("/", 1)[-1], cache_rel)
    (RAW / "works_index.json").write_text(json.dumps(idx, indent=0, sort_keys=True))


def load_work(wid: str):
    """Cached OpenAlex work record: Stage 1 single lookups (data/raw/works/{id}.json) or the
    Stage 2 search response that returned it (via data/raw/works_index.json)."""
    plain = RAW / "works" / f"{wid}.json"
    if plain.exists():
        return json.loads(plain.read_text())
    rel = _index()[wid]
    if rel not in _FILE_CACHE:
        if len(_FILE_CACHE) > 400:
            _FILE_CACHE.clear()
        body = _read_cache(ROOT / rel)
        _FILE_CACHE[rel] = {w["id"].rsplit("/", 1)[-1]: w for w in body["results"]}
    return _FILE_CACHE[rel][wid]
