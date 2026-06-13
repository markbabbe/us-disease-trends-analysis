#!/usr/bin/env python3
"""Fetch recent national case counts live from the CDC NNDSS open-data API.

Source: CDC "NNDSS Weekly Data" (data.cdc.gov resource x9gk-5huc), the Socrata
API behind the MMWR weekly notifiable-disease tables.

IMPORTANT CAVEATS (see data/SOURCES.md for the full discussion):
  * This API only covers ~2022-present. It does NOT contain the deep historical
    (1900-2020) series this project depends on — those live in scanned MMWR
    annual summaries, the Pink Book Appendix E (PDF), and NCHS Vital Statistics.
  * These are WEEKLY PROVISIONAL surveillance counts. The column `m3` is the
    cumulative year-to-date count; the year-end value (max over weeks) is used
    here as the annual total. Provisional counts can differ from the finalized
    MMWR annual summary by a few percent, and the current year is partial.
  * Rows exist at several geographic levels (state, region, "Total",
    "U.S. Residents"). Only `states = Total` is summed to avoid double-counting.

Usage:  python3 scripts/fetch_cdc_nndss.py
Writes: data/cdc_nndss_recent.csv
"""
import csv
import json
import os
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
BASE = "https://data.cdc.gov/resource/x9gk-5huc.json"

# Disease -> list of NNDSS label prefixes to sum (handles split sub-labels)
DISEASES = {
    "measles": ["Measles"],          # Measles, Imported + Measles, Indigenous
    "pertussis": ["Pertussis"],
    "polio": ["Poliomyelitis"],      # paralytic; typically none
}


def soql(params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def annual_totals(prefix):
    """Year -> summed year-end cumulative (max m3 per sub-label), national only."""
    rows = soql({
        "$select": "year,label,max(m3)",
        "$where": f"label like '{prefix}%' and upper(states)='TOTAL'",
        "$group": "year,label",
        "$order": "year",
    })
    totals = {}
    for r in rows:
        yr = int(r["year"])
        val = r.get("max_m3")
        if val is None:
            continue
        totals[yr] = totals.get(yr, 0) + int(round(float(val)))
    return totals


def main():
    by_year = {}
    for disease, prefixes in DISEASES.items():
        merged = {}
        for p in prefixes:
            for yr, v in annual_totals(p).items():
                merged[yr] = merged.get(yr, 0) + v
        for yr, v in merged.items():
            by_year.setdefault(yr, {})[disease] = v

    out = os.path.join(DATA, "cdc_nndss_recent.csv")
    years = sorted(by_year)
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "measles", "pertussis", "polio", "source"])
        for yr in years:
            d = by_year[yr]
            w.writerow([yr, d.get("measles", ""), d.get("pertussis", ""),
                        d.get("polio", 0),
                        "CDC NNDSS API x9gk-5huc (provisional, cumulative m3)"])
    print("wrote", os.path.relpath(out, os.path.join(HERE, "..")))
    for yr in years:
        print(" ", yr, by_year[yr])


if __name__ == "__main__":
    main()
