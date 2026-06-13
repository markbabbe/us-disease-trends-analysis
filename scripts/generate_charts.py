#!/usr/bin/env python3
"""Generate charts for the U.S. vaccine-preventable disease trend analysis.

Reads CSVs in ../data, interpolates Census population to each reporting year,
computes incidence per 100,000, and writes PNG charts to ../charts.

Data provenance: CDC MMWR Summary of Notifiable Diseases, CDC Pinkbook
Appendix E, NCHS Vital Statistics, U.S. Census Bureau. See data/SOURCES.md.
"""
import csv
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "charts")
os.makedirs(OUT, exist_ok=True)

VACCINE = {
    "polio": [(1955, "Salk IPV"), (1961, "Sabin OPV")],
    "pertussis": [(1948, "Whole-cell DTP"), (1997, "DTaP switch")],
    "measles": [(1963, "Measles vaccine"), (1971, "MMR"), (1989, "2-dose")],
}


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


def to_int(v):
    v = (v or "").strip()
    return int(v) if v else None


def load_population():
    rows = read_csv("us_population.csv")
    yrs = np.array([int(r["year"]) for r in rows])
    pop = np.array([int(r["population"]) for r in rows])
    return yrs, pop


def pop_for(year, yrs, pop):
    return float(np.interp(year, yrs, pop))


def series(rows, field):
    out = []
    for r in rows:
        val = to_int(r.get(field))
        if val is not None:
            out.append((int(r["year"]), val))
    out.sort()
    return [y for y, _ in out], [v for _, v in out]


def add_vaccine_lines(ax, disease):
    for yr, label in VACCINE.get(disease, []):
        ax.axvline(yr, color="#888", linestyle="--", linewidth=1)
        ax.text(yr, ax.get_ylim()[1] * 0.92, f" {label} {yr}",
                rotation=90, va="top", ha="left", fontsize=8, color="#444")


def drop_zeros(yrs, vals):
    """Log scale cannot show zeros; drop those points."""
    pairs = [(y, v) for y, v in zip(yrs, vals) if v and v > 0]
    return [y for y, _ in pairs], [v for _, v in pairs]


def cases_chart(disease, rows, case_field, title):
    yrs, cases = series(rows, case_field)
    yrs, cases = drop_zeros(yrs, cases)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(yrs, cases, "-o", color="#c0392b", markersize=4, linewidth=1.5)
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel("Reported cases (log scale)")
    ax.set_yscale("log")
    ax.grid(True, which="both", alpha=0.3)
    add_vaccine_lines(ax, disease)
    fig.tight_layout()
    p = os.path.join(OUT, f"{disease}_cases.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def incidence_chart(disease, rows, case_field, title, pyrs, pop):
    yrs, cases = series(rows, case_field)
    yrs, cases = drop_zeros(yrs, cases)
    inc = [c / pop_for(y, pyrs, pop) * 100000 for y, c in zip(yrs, cases)]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(yrs, inc, "-o", color="#2c6fbb", markersize=4, linewidth=1.5)
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel("Incidence per 100,000 (log scale)")
    ax.set_yscale("log")
    ax.grid(True, which="both", alpha=0.3)
    add_vaccine_lines(ax, disease)
    fig.tight_layout()
    p = os.path.join(OUT, f"{disease}_incidence.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def deaths_chart(disease, rows, title):
    yrs, deaths = series(rows, "deaths")
    if not yrs:
        return None
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(yrs, deaths, "-o", color="#555", markersize=4, linewidth=1.5)
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel("Reported deaths")
    ax.grid(True, alpha=0.3)
    add_vaccine_lines(ax, disease)
    fig.tight_layout()
    p = os.path.join(OUT, f"{disease}_deaths.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def cfr_chart(disease, rows, case_field, title):
    """Case fatality rate (%) for years where both cases and deaths exist."""
    pts = []
    for r in rows:
        c = to_int(r.get(case_field))
        d = to_int(r.get("deaths"))
        if c and d is not None and c > 0:
            pts.append((int(r["year"]), d / c * 100))
    if len(pts) < 2:
        return None
    pts.sort()
    yrs = [y for y, _ in pts]
    cfr = [v for _, v in pts]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(yrs, cfr, "-o", color="#8e44ad", markersize=4, linewidth=1.5)
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel("Case fatality rate (%)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    p = os.path.join(OUT, f"{disease}_cfr.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def combined_incidence(pyrs, pop, configs):
    fig, ax = plt.subplots(figsize=(11, 6))
    colors = {"polio": "#27ae60", "pertussis": "#e67e22", "measles": "#c0392b"}
    for disease, rows, field, label in configs:
        yrs, cases = series(rows, field)
        yrs, cases = drop_zeros(yrs, cases)
        inc = [c / pop_for(y, pyrs, pop) * 100000 for y, c in zip(yrs, cases)]
        ax.plot(yrs, inc, "-o", markersize=3, linewidth=1.5,
                color=colors[disease], label=label)
    ax.set_yscale("log")
    ax.set_title("Reported incidence per 100,000, U.S. — three diseases")
    ax.set_xlabel("Year")
    ax.set_ylabel("Incidence per 100,000 (log scale)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    p = os.path.join(OUT, "combined_incidence.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def early_mortality_chart():
    rows = read_csv("early_mortality_rates.csv")
    yrs = [int(r["year"]) for r in rows]
    measles = [float(r["measles_death_rate"]) for r in rows]
    pertussis = [float(r["pertussis_death_rate"]) for r in rows]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(yrs, measles, "-o", color="#c0392b", label="Measles")
    ax.plot(yrs, pertussis, "-o", color="#e67e22", label="Pertussis")
    ax.axvline(1948, color="#888", linestyle="--", linewidth=1)
    ax.text(1948, ax.get_ylim()[1] * 0.9, " DTP routine ~1948",
            rotation=90, va="top", fontsize=8, color="#444")
    ax.set_title("Approximate death rate per 100,000, U.S., 1900-1960\n"
                 "(both vaccines licensed after this window: measles 1963)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Deaths per 100,000 population")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    p = os.path.join(OUT, "early_mortality_rates.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def main():
    pyrs, pop = load_population()
    measles = read_csv("measles.csv")
    polio = read_csv("polio.csv")
    pertussis = read_csv("pertussis.csv")

    made = []
    made.append(cases_chart("measles", measles, "reported_cases",
                            "Measles — reported cases, U.S."))
    made.append(incidence_chart("measles", measles, "reported_cases",
                                "Measles — incidence per 100,000, U.S.", pyrs, pop))
    made.append(deaths_chart("measles", measles, "Measles — reported deaths, U.S."))
    made.append(cfr_chart("measles", measles, "reported_cases",
                          "Measles — case fatality rate, U.S."))

    made.append(cases_chart("polio", polio, "total_cases",
                            "Poliomyelitis — reported cases, U.S."))
    made.append(incidence_chart("polio", polio, "total_cases",
                                "Poliomyelitis — incidence per 100,000, U.S.", pyrs, pop))
    made.append(deaths_chart("polio", polio, "Poliomyelitis — reported deaths, U.S."))

    made.append(cases_chart("pertussis", pertussis, "reported_cases",
                            "Pertussis — reported cases, U.S."))
    made.append(incidence_chart("pertussis", pertussis, "reported_cases",
                                "Pertussis — incidence per 100,000, U.S.", pyrs, pop))
    made.append(deaths_chart("pertussis", pertussis, "Pertussis — reported deaths, U.S."))

    made.append(early_mortality_chart())

    made.append(combined_incidence(pyrs, pop, [
        ("polio", polio, "total_cases", "Polio (total)"),
        ("pertussis", pertussis, "reported_cases", "Pertussis"),
        ("measles", measles, "reported_cases", "Measles"),
    ]))

    for p in made:
        if p:
            print("wrote", os.path.relpath(p, os.path.join(HERE, "..")))


if __name__ == "__main__":
    main()
