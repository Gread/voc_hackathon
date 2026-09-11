"""CFPB Consumer Complaint search API: month-by-month pull with a raw JSONL cache.

Verified API facts: JSON by default (never pass format=json), default httpx user agent,
Elasticsearch-shaped response (hits.hits[i]._source), deep paging via search_after
built from the last hit's "sort" values (the frm offset does not paginate).
"""
from __future__ import annotations

import random
import time
from pathlib import Path
from typing import Any, Callable, Iterator

import httpx

from voc.ingest.normalize import company_slug, month_bounds, month_range, read_jsonl, write_jsonl_atomic
from voc.paths import Paths

BASE_URL = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
PRODUCTS = [
    "Checking or savings account",
    "Credit card",
    "Mortgage",
    "Money transfer, virtual currency, or money service",
    "Vehicle loan or lease",
    "Payday loan, title loan, personal loan, or advance loan",
    "Debt collection",
    "Prepaid card",
    "Student loan",
]
PAGE_SIZE = 1000
RETRY_STATUSES = {429, 500, 502, 503, 504}
MAX_RETRIES = 5


def make_client(timeout: float = 60.0) -> httpx.Client:
    return httpx.Client(timeout=timeout)


def base_params(company: str, products: list[str], date_min: str, date_max: str) -> dict[str, Any]:
    return {
        "has_narrative": "true",
        "company": company,
        "product": list(products),
        "date_received_min": date_min,
        "date_received_max": date_max,
    }


def get_json(client: httpx.Client, params: dict[str, Any], *, sleep: Callable[[float], None] = time.sleep) -> dict:
    """GET with retries on 429/5xx (exponential backoff with jitter)."""
    for attempt in range(MAX_RETRIES + 1):
        response = client.get(BASE_URL, params=params)
        if response.status_code in RETRY_STATUSES and attempt < MAX_RETRIES:
            sleep(min(60.0, 2.0 ** attempt + random.random()))
            continue
        response.raise_for_status()
        return response.json()
    raise RuntimeError("unreachable")


def iter_pages(client: httpx.Client, company: str, products: list[str], month: str, *,
               size: int = PAGE_SIZE, pause: float = 1.0,
               sleep: Callable[[float], None] = time.sleep) -> Iterator[list[dict]]:
    """Yield pages of _source dicts for one month, following search_after until exhausted."""
    date_min, date_max = month_bounds(month)
    params = base_params(company, products, date_min, date_max)
    params.update({"size": size, "no_aggs": "true", "sort": "created_date_desc"})
    search_after: str | None = None
    while True:
        if search_after:
            params["search_after"] = search_after
        hits = get_json(client, params, sleep=sleep).get("hits", {}).get("hits", [])
        if not hits:
            return
        yield [h["_source"] for h in hits]
        if len(hits) < size or not hits[-1].get("sort"):
            return
        search_after = "_".join(str(x) for x in hits[-1]["sort"])
        sleep(pause)


def fetch_month(client: httpx.Client, company: str, products: list[str], month: str, **kw) -> list[dict]:
    """All narrative complaints of a company received in one month, deduplicated by complaint_id.

    Both API date bounds are inclusive by calendar day, so the boundary day of the next month
    comes back too; rows are filtered to the month so raw files never overlap.
    """
    seen: set[str] = set()
    out: list[dict] = []
    for page in iter_pages(client, company, products, month, **kw):
        for src in page:
            cid = str(src.get("complaint_id"))
            if str(src.get("date_received") or "")[:7] == month and cid not in seen:
                seen.add(cid)
                out.append(src)
    return out


def fetch_aggregations(client: httpx.Client, company: str, products: list[str], month: str,
                       *, sleep: Callable[[float], None] = time.sleep) -> dict:
    """size=0 without no_aggs returns hits.total plus product/state/tags/submitted_via aggregations."""
    date_min, date_max = month_bounds(month)
    params = base_params(company, products, date_min, date_max)
    params["size"] = 0
    return get_json(client, params, sleep=sleep)


# --- raw cache ------------------------------------------------------------------------

def raw_dir(paths: Paths, company: str) -> Path:
    return paths.raw_cfpb / company_slug(company)


def raw_month_path(paths: Paths, company: str, month: str) -> Path:
    return raw_dir(paths, company) / f"{month}.jsonl"


def read_raw_month(paths: Paths, company: str, month: str) -> list[dict]:
    return list(read_jsonl(raw_month_path(paths, company, month)))


def read_raw_window(paths: Paths, company: str, start: str, end: str) -> dict[str, list[dict]]:
    """{month: rows} for cached months only; missing months are absent from the dict."""
    out: dict[str, list[dict]] = {}
    for month in month_range(start, end):
        path = raw_month_path(paths, company, month)
        if path.exists():
            out[month] = list(read_jsonl(path))
    return out


def pull(paths: Paths, company: str, start: str, end: str, *, force: bool = False,
         client: httpx.Client | None = None, products: list[str] | None = None,
         pause: float = 1.0, sleep: Callable[[float], None] = time.sleep) -> dict[str, int]:
    """Pull every month in the window into data/raw/cfpb/<slug>/<YYYY-MM>.jsonl; returns counts."""
    products = products or PRODUCTS
    own_client = client is None
    client = client or make_client()
    counts: dict[str, int] = {}
    try:
        for month in month_range(start, end):
            path = raw_month_path(paths, company, month)
            if path.exists() and not force:
                counts[month] = sum(1 for _ in read_jsonl(path))
                print(f"{month}  {counts[month]:6d}  (cached)")
                continue
            rows = fetch_month(client, company, products, month, pause=pause, sleep=sleep)
            write_jsonl_atomic(path, rows)
            counts[month] = len(rows)
            print(f"{month}  {counts[month]:6d}")
            sleep(pause)
    finally:
        if own_client:
            client.close()
    print(f"total  {sum(counts.values()):6d}  -> {raw_dir(paths, company)}")
    return counts
