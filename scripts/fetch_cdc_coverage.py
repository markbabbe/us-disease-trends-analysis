#!/usr/bin/env python3
"""Fetch recent U.S. childhood vaccination coverage from the CDC NIS API.

Source: CDC "Vaccination Coverage among Young Children (0-35 Months)"
(data.cdc.gov resource fhky-rtsk), from the National Immunization Survey (NIS).

SCOPE / CAVEAT (see data/SOURCES.md and README "Coverage" section):
  * This dataset begins around birth-year 2011. The NIS itself started in 1994.
  * There is NO clean national annual coverage time series before ~1994 — the
    critical early-uptake decades (polio 1955+, measles 1963+) are documented
    only in published MMWR historical reports, given here as milestone anchors
    in data/coverage_milestones.md, NOT as an API series.
  * Coverage is for children by age 24 months (the standard milestone).

Usage:  python3 scripts/fetch_cdc_coverage.py
Writes: data/coverage.csv
"""
import csv
import json
import os
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
BASE = "https://data.cdc.gov/resource/fhky-rtsk.json"

# label -> (vaccine value, dose value) ; dose "" means any/only-one
SERIES = {
    "measles_mmr": ("≥1 Dose MMR", ""),
    "pertussis_dtap": ("DTaP", "≥3 Doses"),
    "polio": ("Polio", "≥3 Doses"),
}


def soql(params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def fetch(vaccine, dose):
    where = (f"vaccine='{vaccine}' and geography='United States' "
             f"and dimension_type='Age' and dimension='24 Months'")
    if dose:
        where += f" and dose='{dose}'"
    rows = soql({"$select": "year_season,coverage_estimate,dose",
                 "$where": where, "$order": "year_season"})
    out = {}
    for r in rows:
        ys = r.get("year_season", "")
        if len(ys) != 4:           # keep single calendar (birth) years only
            continue
        if dose and r.get("dose") != dose:
            continue
        out[int(ys)] = float(r["coverage_estimate"])
    return out


def main():
    series = {label: fetch(v, d) for label, (v, d) in SERIES.items()}
    years = sorted(set().union(*[s.keys() for s in series.values()]))
    out = os.path.join(DATA, "coverage.csv")
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "measles_mmr", "pertussis_dtap", "polio", "source"])
        for yr in years:
            w.writerow([yr,
                        series["measles_mmr"].get(yr, ""),
                        series["pertussis_dtap"].get(yr, ""),
                        series["polio"].get(yr, ""),
                        "CDC NIS fhky-rtsk (by 24 months)"])
    print("wrote", os.path.relpath(out, os.path.join(HERE, "..")))
    for yr in years:
        print(" ", yr, {k: series[k].get(yr) for k in series})


if __name__ == "__main__":
    main()
