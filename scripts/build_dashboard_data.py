#!/usr/bin/env python3
"""Emit docs/data.js for the interactive dashboard from the CSVs in data/.

Single source of truth: the same CSVs that feed the static charts. Computes
incidence per 100,000 (Census population, interpolated) and case fatality rate.
"""
import csv
import json
import os
import shutil

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
DOCS = os.path.join(HERE, "..", "docs")
os.makedirs(DOCS, exist_ok=True)


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


def to_int(v):
    v = (v or "").strip()
    return int(v) if v else None


def load_pop():
    rows = read_csv("us_population.csv")
    return (np.array([int(r["year"]) for r in rows]),
            np.array([int(r["population"]) for r in rows]))


def early_rates(disease):
    """Early-century deaths per 100,000 from early_mortality_rates.csv."""
    col = {"measles": "measles_death_rate", "pertussis": "pertussis_death_rate"}.get(disease)
    if not col:
        return {}
    return {int(r["year"]): float(r[col]) for r in read_csv("early_mortality_rates.csv")}


# Diseases whose counts are children-under-5 only -> use the <5 population as denominator.
UNDER5 = {"hib", "pcv", "rotavirus"}


def load_pop_under5():
    rows = read_csv("us_population_under5.csv")
    return (np.array([int(r["year"]) for r in rows]),
            np.array([int(r["population"]) for r in rows]))


def build(rows, case_field, disease):
    pyrs, pop = load_pop_under5() if disease in UNDER5 else load_pop()
    early = early_rates(disease)
    out = {}
    for r in rows:
        y = int(r["year"])
        cases = to_int(r.get(case_field))
        deaths = to_int(r.get("deaths"))
        hosp = to_int(r.get("hospitalizations"))
        p = float(np.interp(y, pyrs, pop))
        inc = round(cases / p * 100000, 4) if cases is not None else None
        cfr = round(deaths / cases * 100, 4) if (cases and deaths is not None and cases > 0) else None
        death_rate = round(deaths / p * 100000, 4) if deaths is not None else None
        hosp_rate = round(hosp / p * 100000, 4) if hosp is not None else None
        out[y] = {"year": y, "cases": cases, "deaths": deaths, "incidence": inc,
                  "cfr": cfr, "death_rate": death_rate, "hosp_rate": hosp_rate,
                  "note": r.get("notes", "")}
    # Backfill early-era death rates (1900-1930) where the count series lacks them.
    for y, rate in early.items():
        rec = out.get(y)
        if rec is None:
            out[y] = {"year": y, "cases": None, "deaths": None, "incidence": None,
                      "cfr": None, "death_rate": rate, "hosp_rate": None,
                      "note": "Early death rate (approx)"}
        elif rec["death_rate"] is None:
            rec["death_rate"] = rate
    return [out[y] for y in sorted(out)]


def early():
    rows = read_csv("early_mortality_rates.csv")
    return [{"year": int(r["year"]),
             "measles": float(r["measles_death_rate"]),
             "pertussis": float(r["pertussis_death_rate"])} for r in rows]


def chronic():
    """Chronic-illness prevalence + childhood vaccine count, by year (long format)."""
    out = {}
    for r in read_csv("chronic_illness.csv"):
        out.setdefault(r["series"], []).append(
            {"year": int(r["year"]), "value": float(r["value"])})
    return out


def lamerato():
    """Per-condition prevalence (%) by group, Lamerato/Henry Ford study."""
    return [{"condition": r["condition"], "vax": float(r["vax_pct"]),
             "novx": float(r["novx_pct"]), "vax_n": int(r["vax_n"]),
             "novx_n": int(r["novx_n"])} for r in read_csv("lamerato_conditions.csv")]


def coverage_levels():
    """CDC Pink Book Appendix E coverage levels, 1962-2016 (all vaccines)."""
    cols = ("dtp3", "dtp4", "polio3", "mmr", "hib3", "var", "pcv3", "hepb3", "rota")
    out = []
    for r in read_csv("coverage_levels_pinkbook.csv"):
        rec = {"year": int(r["year"])}
        for k in cols:
            v = (r.get(k) or "").strip()
            rec[k] = float(v) if v else None
        out.append(rec)
    return out


def coverage():
    """Merge approximate historical anchors with live modern NIS data."""
    def f(v):
        v = (v or "").strip()
        return float(v) if v else None
    series = {"measles": {}, "pertussis": {}, "polio": {}}
    for r in read_csv("coverage_historical.csv"):
        y = int(r["year"])
        for d, col in [("measles", "measles_mmr"), ("pertussis", "pertussis_dtap"), ("polio", "polio")]:
            v = f(r[col])
            if v is not None:
                series[d][y] = {"year": y, "value": v, "approx": True}
    for r in read_csv("coverage.csv"):
        y = int(r["year"])
        for d, col in [("measles", "measles_mmr"), ("pertussis", "pertussis_dtap"), ("polio", "polio")]:
            v = f(r[col])
            if v is not None:
                series[d][y] = {"year": y, "value": v, "approx": False}
    return {d: [series[d][y] for y in sorted(series[d])] for d in series}


# disease key -> (csv file, case-count column, display name)
DISEASE_CFG = {
    "hepb": ("hepb.csv", "cases", "Hepatitis B"),
    "rotavirus": ("rotavirus.csv", "cases", "Rotavirus"),
    "diphtheria": ("diphtheria.csv", "cases", "Diphtheria"),
    "tetanus": ("tetanus.csv", "cases", "Tetanus"),
    "pertussis": ("pertussis.csv", "reported_cases", "Pertussis"),
    "hib": ("hib.csv", "cases", "Hib"),
    "pcv": ("pcv.csv", "cases", "Pneumococcal (PCV)"),
    "polio": ("polio.csv", "total_cases", "Polio"),
    "measles": ("measles.csv", "reported_cases", "Measles"),
    "mumps": ("mumps.csv", "cases", "Mumps"),
    "rubella": ("rubella.csv", "cases", "Rubella"),
    "meningococcal": ("meningococcal.csv", "cases", "Meningococcal"),
}

VACCINES = {
    "hepb": [{"year": 1981, "label": "HepB vaccine"}, {"year": 1991, "label": "Infant/universal"}],
    "rotavirus": [{"year": 2006, "label": "Rotavirus vaccine"}],
    "hib": [{"year": 1990, "label": "Hib conjugate (infant)"}],
    "pcv": [{"year": 2000, "label": "PCV7"}, {"year": 2010, "label": "PCV13"}],
    "diphtheria": [{"year": 1926, "label": "Toxoid"}, {"year": 1948, "label": "DTP"}],
    "tetanus": [{"year": 1948, "label": "DTP (toxoid)"}],
    "pertussis": [{"year": 1948, "label": "Whole-cell DTP"}, {"year": 1997, "label": "DTaP switch"}],
    "polio": [{"year": 1955, "label": "Salk IPV"}, {"year": 1961, "label": "Sabin OPV"}],
    "measles": [{"year": 1963, "label": "Measles vaccine"}, {"year": 1971, "label": "MMR"},
                {"year": 1989, "label": "2nd dose"}],
    "mumps": [{"year": 1967, "label": "Mumps vaccine"}, {"year": 1971, "label": "MMR"}],
    "rubella": [{"year": 1969, "label": "Rubella vaccine"}, {"year": 1971, "label": "MMR"}],
    "meningococcal": [{"year": 2005, "label": "MenACWY (adolescents)"},
                      {"year": 2011, "label": "16y booster"},
                      {"year": 2015, "label": "MenB"}],
}

# Tabs ordered by the childhood immunization schedule (birth -> 2mo -> 12-15mo)
TABS = [
    {"id": "overview", "label": "Overview", "sub": "home", "diseases": []},
    {"id": "hepb", "label": "HepB", "sub": "birth", "diseases": ["hepb"]},
    {"id": "rv", "label": "Rotavirus", "sub": "2 months", "diseases": ["rotavirus"]},
    {"id": "dtap", "label": "DTaP", "sub": "2 months", "diseases": ["diphtheria", "tetanus", "pertussis"]},
    {"id": "hib", "label": "Hib", "sub": "2 months", "diseases": ["hib"]},
    {"id": "pcv", "label": "PCV", "sub": "2 months", "diseases": ["pcv"]},
    {"id": "ipv", "label": "Polio (IPV)", "sub": "2 months", "diseases": ["polio"]},
    {"id": "mmr", "label": "MMR", "sub": "12-15 months", "diseases": ["measles", "mumps", "rubella"]},
    {"id": "menb", "label": "Meningococcal", "sub": "11-12 years", "diseases": ["meningococcal"]},
    {"id": "chronic", "label": "Chronic illness", "sub": "correlation ≠ causation", "diseases": []},
]


def main():
    data = {
        "vaccines": VACCINES,
        "tabs": TABS,
        "names": {k: v[2] for k, v in DISEASE_CFG.items()},
        "under5": sorted(UNDER5),
        "earlyMortality": early(),
        "coverage": coverage(),
        "coverageLevels": coverage_levels(),
        "chronic": chronic(),
        "lamerato": lamerato(),
    }
    for key, (csvf, field, _name) in DISEASE_CFG.items():
        data[key] = build(read_csv(csvf), field, key)
    path = os.path.join(DOCS, "data.js")
    with open(path, "w") as f:
        f.write("// Auto-generated by scripts/build_dashboard_data.py — do not edit.\n")
        f.write("window.DISEASE_DATA = ")
        json.dump(data, f, indent=2)
        f.write(";\n")
    print("wrote", os.path.relpath(path, os.path.join(HERE, "..")))

    # Copy analytical charts that the dashboard embeds directly (must live in docs/).
    for fname in ["polio_definition_effect.png", "childhood_meningitis.png"]:
        src = os.path.join(HERE, "..", "charts", fname)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(DOCS, fname))
            print("copied", fname, "-> docs/")


if __name__ == "__main__":
    main()
