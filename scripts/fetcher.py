"""One throttled, caching HTTP fetcher for OpenAlex and Crossref.

All network access in this project goes through `Fetcher.get_json`, which:
- runs requests strictly one at a time (no threads, no async);
- waits at least `min_interval` seconds between requests;
- backs off exponentially on 429 / 5xx and network errors, honouring Retry-After;
- caches every raw response body under data/raw/ so runs are reproducible and resumable.

Searches are run through the OpenAlex connector (the keyless public API refuses
list/search requests from this network); single-work lookups by ID are free on the
public API and are fetched here.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"


class Fetcher:
    def __init__(self, min_interval: float = 1.0, max_retries: int = 6):
        self.min_interval = min_interval
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers["User-Agent"] = (
            "literature-map/0.1 (research bibliography; mailto:%s)"
            % os.environ.get("OPENALEX_MAILTO", "unset")
        )
        if os.path.exists(CA_BUNDLE):
            self.session.verify = CA_BUNDLE
        self._last = 0.0
        self.network_calls = 0
        self.cache_hits = 0

    def _wait(self):
        dt = time.monotonic() - self._last
        if dt < self.min_interval:
            time.sleep(self.min_interval - dt)
        self._last = time.monotonic()

    def get_json(self, url: str, params: dict | None, cache_path: Path):
        """Return parsed JSON for url, from cache_path if present. None on 404."""
        if cache_path.exists():
            self.cache_hits += 1
            body = json.loads(cache_path.read_text())
            return None if body.get("_status") == 404 else body
        params = dict(params or {})
        if os.environ.get("OPENALEX_MAILTO") and "openalex.org" in url:
            params["mailto"] = os.environ["OPENALEX_MAILTO"]
        delay = 2.0
        for attempt in range(self.max_retries):
            self._wait()
            self.network_calls += 1
            try:
                r = self.session.get(url, params=params, timeout=60)
            except requests.RequestException as e:
                print(f"  network error {e!r}; retry in {delay:.0f}s", file=sys.stderr)
                time.sleep(delay)
                delay *= 2
                continue
            if r.status_code == 200:
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                cache_path.write_text(r.text)
                return r.json()
            if r.status_code == 404:
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                cache_path.write_text(json.dumps({"_status": 404, "url": r.url}))
                return None
            if r.status_code == 429 or r.status_code >= 500:
                ra = r.headers.get("Retry-After")
                wait = float(ra) if ra and ra.isdigit() and float(ra) < 120 else delay
                if r.status_code == 429 and ra and ra.isdigit() and float(ra) >= 120:
                    raise RuntimeError(f"Rate limited for {ra}s on {r.url}: {r.text[:300]}")
                print(f"  HTTP {r.status_code}; retry in {wait:.0f}s", file=sys.stderr)
                time.sleep(wait)
                delay *= 2
                continue
            raise RuntimeError(f"HTTP {r.status_code} on {r.url}: {r.text[:300]}")
        raise RuntimeError(f"Gave up after {self.max_retries} attempts: {url}")

    def openalex_work(self, wid: str):
        return self.get_json(
            f"https://api.openalex.org/works/{wid}", None, RAW / "works" / f"{wid}.json"
        )

    def crossref_work(self, doi: str):
        safe = doi.replace("/", "_")
        return self.get_json(
            f"https://api.crossref.org/works/{doi}", None, RAW / "crossref" / f"{safe}.json"
        )
