#!/usr/bin/env python3
"""Upgrade measles.csv and pertussis.csv to COMPLETE ANNUAL series from OWID.

Replaces the earlier anchor-based measles/pertussis series so all diseases in the
MMR and DTaP tabs share the same annual granularity.

Sources (Our World in Data; underlying U.S. Public Health Reports + CDC):
  measles cases  -> owid_combined_cases.csv (Measles column), 1919-2025
  measles deaths -> owid_measles_rate.csv (Death rate per 100k x Census pop)
  pertussis      -> owid_pertussis.csv (cases 1922-2022, deaths 1944-2022)
Recent pertussis (2023-2025) appended from cdc_nndss_recent.csv (provisional).
Early measles/pertussis death RATES (1900-1930) remain in early_mortality_rates.csv,
used by the dashboard/early chart.
"""
import csv
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

NOTES_MEASLES = {1963: "Measles vaccine licensed", 1971: "MMR licensed",
                 1989: "2nd dose recommended (after 1989-91 resurgence)",
                 2000: "Elimination declared", 2025: "Large outbreak year"}
NOTES_PERTUSSIS = {1948: "Whole-cell DTP routine", 1997: "Acellular DTaP switch",
                   2012: "Highest since 1955", 2024: "Resurgence (CDC NNDSS, provisional)"}


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


def to_num(v):
    v = (v or "").strip()
    return float(v) if v else None


def write(name, col, rows):
    with open(os.path.join(DATA, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", col, "deaths", "notes"])
        w.writerows(rows)
    nd = sum(1 for r in rows if r[2] != "")
    print(f"wrote data/{name}: {len(rows)} rows ({rows[0][0]}-{rows[-1][0]}), {nd} with deaths")


def main():
    pop_rows = read_csv("us_population.csv")
    pyrs = np.array([int(r["year"]) for r in pop_rows])
    pop = np.array([int(r["population"]) for r in pop_rows])

    # ---- Measles: cases from combined, deaths from death-rate x population ----
    cases = {}
    for r in read_csv("owid_combined_cases.csv"):     # exact counts where present
        y = int(r["Year"])
        if y >= 2026:                                 # 2026 incomplete
            continue
        v = to_num(r.get("Measles"))
        if v is not None:
            cases[y] = round(v)
    deaths = {}
    for r in read_csv("owid_measles_rate.csv"):
        y = int(r["Year"])
        if y >= 2026:
            continue
        p = float(np.interp(y, pyrs, pop))
        dr = to_num(r.get("Death rate"))
        if dr is not None:
            deaths[y] = round(dr * p / 1e5)
        cr = to_num(r.get("Case rate"))               # fill case gaps (e.g. 1926-37)
        if cr is not None and y not in cases:
            cases[y] = round(cr * p / 1e5)
    years = sorted(set(cases) | set(deaths))
    rows = [[y, cases.get(y, ""), deaths.get(y, ""), NOTES_MEASLES.get(y, "")] for y in years]
    write("measles.csv", "reported_cases", rows)

    # ---- Pertussis: cases + deaths from OWID, recent from CDC NNDSS ----
    pc, pd = {}, {}
    for r in read_csv("owid_pertussis.csv"):
        y = int(r["Year"])
        c, d = to_num(r.get("Pertussis cases")), to_num(r.get("Pertussis deaths"))
        if c is not None:
            pc[y] = round(c)
        if d is not None:
            pd[y] = round(d)
    for r in read_csv("cdc_nndss_recent.csv"):       # 2023-2025 provisional
        y = int(r["year"])
        v = to_num(r.get("pertussis"))
        if 2023 <= y <= 2025 and v is not None:       # exclude partial current year
            pc[y] = round(v)
    years = sorted(pc)
    rows = [[y, pc.get(y, ""), pd.get(y, ""), NOTES_PERTUSSIS.get(y, "")] for y in years]
    write("pertussis.csv", "reported_cases", rows)


if __name__ == "__main__":
    main()
