#!/usr/bin/env python3
"""Rebuild data/polio.csv as a COMPLETE ANNUAL series from authoritative rates.

Motivation: the earlier polio.csv used sparse anchor years, so charts drew long
straight interpolations (e.g., a 33-year line for deaths 1916->1949). This script
replaces the 1910-1971 portion with annual data derived from Our World in Data's
U.S. polio death-rate and case-rate series (source: U.S. Public Health Reports
1942 + CDC, processed by OWID), converted to counts using interpolated Census
population. Paralytic-case figures and documented modern events are preserved.

Inputs:  data/polio_owid_rates.csv, data/us_population.csv, data/polio.csv (prev)
Output:  data/polio.csv  (overwritten)
"""
import csv
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

# Documented modern rows kept verbatim (post-1971 specific events, not annual rates)
MODERN = {
    1979: ("26", "", "", "Last endemic wild-virus outbreak (Amish)"),
    1990: ("7", "7", "", "Vaccine-associated paralytic polio era"),
    2000: ("0", "0", "0", "OPV discontinued in US"),
    2005: ("4", "0", "0", "Importation into unvaccinated community"),
    2022: ("1", "1", "0", "Vaccine-derived case (Rockland County NY)"),
}


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


def main():
    pop_rows = read_csv("us_population.csv")
    pyrs = np.array([int(r["year"]) for r in pop_rows])
    pop = np.array([int(r["population"]) for r in pop_rows])

    # Preserve paralytic_cases and notes from the previous compilation.
    prev = {int(r["year"]): r for r in read_csv("polio.csv")}

    out = []
    for r in read_csv("polio_owid_rates.csv"):
        y = int(r["Year"])
        if y > 1971:                      # modern years handled separately
            continue
        p = float(np.interp(y, pyrs, pop))
        dr = r["Polio death rate"].strip()
        cr = r["Polio case rate"].strip()
        deaths = round(float(dr) * p / 1e5) if dr else ""
        cases = round(float(cr) * p / 1e5) if cr else ""
        prv = prev.get(y, {})
        paralytic = (prv.get("paralytic_cases") or "").strip()
        # Paralytic anchors come from a different source; drop any that exceed the
        # annual total (small rounding differences would otherwise look wrong).
        if paralytic and cases != "" and int(paralytic) > cases:
            paralytic = ""
        note = (prv.get("notes") or "").strip()
        out.append([y, cases, paralytic, deaths, note])

    for y in sorted(MODERN):
        tc, par, de, note = MODERN[y]
        out.append([y, tc, par, de, note])

    out.sort(key=lambda x: x[0])
    with open(os.path.join(DATA, "polio.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "total_cases", "paralytic_cases", "deaths", "notes"])
        w.writerows(out)
    n_deaths = sum(1 for r in out if r[3] != "")
    print(f"wrote data/polio.csv: {len(out)} rows, {n_deaths} with deaths "
          f"({out[0][0]}-{out[-1][0]})")


if __name__ == "__main__":
    main()
