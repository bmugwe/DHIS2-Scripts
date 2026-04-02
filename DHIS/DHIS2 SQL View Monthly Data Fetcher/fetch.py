#!/usr/bin/env python3
"""
DHIS2 SQL View Monthly Data Fetcher
====================================
Fetches monthly data from a DHIS2 SQL View API concurrently.
Covers 2010–2025, one request per month, saves per-year CSVs
and a combined all-data CSV.

Usage:
    python dhis2_sqlview_fetch.py

Configuration:
    Edit the CONFIG block below or set environment variables.
"""

import os
import csv
import time
import logging
import calendar
from io import StringIO
from pathlib import Path
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.auth import HTTPBasicAuth

# ─────────────────────────────────────────────
#  CONFIGURATION  ← Edit these values
# ─────────────────────────────────────────────
CONFIG = {
    # Base DHIS2 URL (no trailing slash)
    "base_url": os.getenv("KHIS", ""),

    # SQL View UID  (get from: Maintenance → SQL Views → copy the UID from the URL)
    "sqlview_uid": os.getenv("DHIS2_SQLVIEW_UID", "m8oTYQH2MA3"),

    # Basic Auth credentials
    "username": os.getenv("KHIS_USERNAME", ""),
    "password": os.getenv("KHIS_PASSWORD", ""),

    # Date range (inclusive, by year)
    "year_start": 2024,
    "year_end":   2026,

    # Concurrency: number of parallel month-requests per year
    # Keep ≤ 6 to be respectful to the DHIS2 server
    "max_workers": 6,

    # Retry settings
    "max_retries": 3,
    "retry_delay_seconds": 5,

    # Output directory
    "output_dir": "HTS Data Benzer",

    # Request timeout in seconds
    "timeout": 120,

    # Page size (DHIS2 default max is 50000)
    "page_size": 100000,
    
    # Dataset Name
    "dataset_name": "HTS Data Benzer",
}
# ─────────────────────────────────────────────

# ── Logging setup ────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def build_url(cfg: dict) -> str:
    """Construct the SQL View data endpoint URL."""
    return (
        f"https://{cfg['base_url']}/api/sqlViews/"
        f"{cfg['sqlview_uid']}/data.csv"
    )


def fetch_month(
    url: str,
    auth: HTTPBasicAuth,
    year: int,
    month: int,
    cfg: dict,
) -> tuple[str, list[dict], list[str]]:
    """
    Fetch data for a single month from the SQL View API.

    The SQL View accepts var=VAR_NAME:value pairs for variable substitution.
    Adjust var names (date_start / date_end) to match your SQL View variable
    names exactly as defined in DHIS2 Maintenance → SQL View.

    Returns:
        (label, rows, fieldnames)  where label = "YYYY-MM"
    """
    last_day   = calendar.monthrange(year, month)[1]
    date_start = date(year, month, 1).strftime("%Y-%m-%d")
    date_end   = date(year, month, last_day).strftime("%Y-%m-%d")
    label      = f"{year}-{month:02d}"

    params = {
        "var":      [f"date_start:{date_start}", f"date_end:{date_end}"],
        "pageSize": cfg["page_size"],
        "paging":   "false",          # disable paging to get all rows at once
    }

    for attempt in range(1, cfg["max_retries"] + 1):
        try:
            log.info(f"  → Fetching {label}  [{date_start} – {date_end}]  (attempt {attempt})")
            resp = requests.get(
                url,
                params=params,
                auth=auth,
                timeout=cfg["timeout"],
            )
            resp.raise_for_status()

            # Parse CSV response
            reader    = csv.DictReader(StringIO(resp.text))
            rows      = list(reader)
            fieldnames = reader.fieldnames or []

            # Stamp each row with the period for traceability
            for row in rows:
                row.setdefault("_fetch_period", label)

            log.info(f"  ✓ {label}  →  {len(rows):,} rows")
            return label, rows, list(fieldnames)

        except requests.exceptions.HTTPError as e:
            log.warning(f"  ✗ {label}  HTTP {e.response.status_code}: {e}")
        except requests.exceptions.RequestException as e:
            log.warning(f"  ✗ {label}  Request error: {e}")

        if attempt < cfg["max_retries"]:
            log.info(f"    Retrying in {cfg['retry_delay_seconds']}s …")
            time.sleep(cfg["retry_delay_seconds"])

    log.error(f"  ✗ {label}  FAILED after {cfg['max_retries']} attempts — skipped.")
    return label, [], []


def fetch_year(
    url: str,
    auth: HTTPBasicAuth,
    year: int,
    cfg: dict,
) -> list[dict]:
    """
    Concurrently fetch all 12 months for a given year.
    Returns a combined list of rows sorted by month.
    """
    log.info(f"\n{'═'*55}")
    log.info(f"  Processing year: {year}")
    log.info(f"{'═'*55}")

    year_rows:   list[dict]  = []
    all_fields:  list[str]   = []
    month_buffer: dict[str, list[dict]] = {}

    with ThreadPoolExecutor(max_workers=cfg["max_workers"]) as executor:
        futures = {
            executor.submit(fetch_month, url, auth, year, month, cfg): month
            for month in range(1, 13)
        }
        for future in as_completed(futures):
            label, rows, fields = future.result()
            month_buffer[label] = rows
            if fields and not all_fields:
                all_fields = fields

    # Re-assemble in chronological month order
    for month in range(1, 13):
        label = f"{year}-{month:02d}"
        year_rows.extend(month_buffer.get(label, []))

    return year_rows, all_fields


def save_csv(filepath: Path, rows: list[dict], fieldnames: list[str]) -> None:
    """Write rows to a CSV file."""
    if not rows:
        log.warning(f"  No data to write → {filepath.name}")
        return

    # Ensure _fetch_period appears last (cosmetic)
    if "_fetch_period" in fieldnames:
        fieldnames = [f for f in fieldnames if f != "_fetch_period"] + ["_fetch_period"]
    elif rows and "_fetch_period" in rows[0]:
        fieldnames = list(fieldnames) + ["_fetch_period"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    log.info(f"  💾 Saved  {filepath.name}  ({len(rows):,} rows)")


def main():
    cfg        = CONFIG
    output_dir = Path(cfg["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    url  = build_url(cfg)
    auth = HTTPBasicAuth(cfg["username"], cfg["password"])

    log.info("DHIS2 SQL View Fetcher")
    log.info(f"  Endpoint   : {url}")
    log.info(f"  SQL View   : {cfg['sqlview_uid']}")
    log.info(f"  Years      : {cfg['year_start']} – {cfg['year_end']}")
    log.info(f"  Workers    : {cfg['max_workers']} concurrent months/year")
    log.info(f"  Output dir : {output_dir.resolve()}")

    all_rows:    list[dict] = []
    all_fields:  list[str]  = []

    for year in range(cfg["year_start"], cfg["year_end"] + 1):
        year_rows, fields = fetch_year(url, auth, year, cfg)

        # Persist all_fields from the first non-empty year
        if fields and not all_fields:
            all_fields = fields

        # Save per-year file
        year_file = output_dir / f"dhis2_data_{year}.csv"
        save_csv(year_file, year_rows, list(all_fields))

        all_rows.extend(year_rows)

    # Save combined file
    log.info(f"\n{'─'*55}")
    log.info("  Writing combined output …")
    combined_file = output_dir / f"dhis2_{cfg['dataset_name']}_{cfg['year_start']}_{cfg['year_end']}.csv"
    save_csv(combined_file, all_rows, list(all_fields))

    log.info(f"\n✅  Done!  Total rows: {len(all_rows):,}")
    log.info(f"   Per-year files + combined CSV in → {output_dir.resolve()}")


if __name__ == "__main__":
    main()