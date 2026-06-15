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
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter


def _plain(v, _pos):
    """Format a log tick as a plain number: 0.001, 0.01, 0.1, 1, 10, 1,000."""
    if v <= 0:
        return ""
    if v >= 1:
        return f"{v:,.0f}"
    return ("%g" % v)


def tidy_log_yaxis(ax):
    """Make a log y-axis readable: evenly spaced decade ticks, plain-number
    labels, bold major gridlines, faint minor ones."""
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(LogLocator(base=10))
    ax.yaxis.set_major_formatter(FuncFormatter(_plain))
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=tuple(np.arange(2, 10) * 0.1)))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, which="major", alpha=0.4)
    ax.grid(True, which="minor", alpha=0.08)


def tidy_linear_yaxis(ax):
    """Linear y-axis from 0 with thousands separators — shows the true drop-off."""
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda v, _: f"{v:,.0f}" if (abs(v) >= 1 or v == 0) else ("%g" % v)))
    ax.grid(True, alpha=0.3)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "charts")
os.makedirs(OUT, exist_ok=True)

VACCINE = {
    "polio": [(1955, "Salk IPV"), (1961, "Sabin OPV")],
    "pertussis": [(1948, "Whole-cell DTP"), (1997, "DTaP switch")],
    "measles": [(1963, "Measles vaccine"), (1971, "MMR"), (1989, "2-dose")],
    "hepb": [(1981, "HepB vaccine"), (1991, "Infant/universal")],
    "diphtheria": [(1948, "DTP")],
    "tetanus": [(1948, "DTP (toxoid)")],
    "mumps": [(1967, "Mumps vaccine"), (1971, "MMR")],
    "rubella": [(1969, "Rubella vaccine"), (1971, "MMR")],
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


# Periods where the case definition / classification changed materially.
DEFINITION_CHANGE = {
    "polio": (1954, 1958,
              "Case definition tightened:\nresidual-paralysis requirement;\nenteroviruses reclassified out"),
}


def add_definition_marker(ax, disease):
    if disease not in DEFINITION_CHANGE:
        return
    x0, x1, label = DEFINITION_CHANGE[disease]
    ax.axvspan(x0, x1, color="#7b2d8e", alpha=0.18, zorder=0)
    trans = ax.get_xaxis_transform()  # x in data coords, y in axes fraction
    ax.text((x0 + x1) / 2, 0.45, label, rotation=90, ha="center", va="center",
            fontsize=7, color="#5b2270", transform=trans, zorder=5)


# Treatment milestones that lowered case fatality independent of incidence.
# (year, short label) — full detail in data/treatment_milestones.md
TREATMENT = {
    "polio": [(1928, "Iron lung (Boston)"),
              (1952, "Positive-pressure ventilation /\nfirst ICU (Copenhagen)")],
    "measles": [(1945, "Antibiotics widespread\n(penicillin)")],
    "pertussis": [(1945, "Antibiotics"), (1965, "Infant intensive care\n(NICU)")],
}


def add_treatment_marker(ax, disease):
    trans = ax.get_xaxis_transform()
    for yr, label in TREATMENT.get(disease, []):
        ax.axvline(yr, color="#159a8c", linestyle=":", linewidth=1.6)
        ax.text(yr, 0.04, " " + label, rotation=90, ha="left", va="bottom",
                fontsize=7, color="#0e6b61", transform=trans, zorder=5)


def add_antibiotic_band(ax):
    """Shade the era when antibiotics became widely available (sulfa -> penicillin)."""
    ax.axvspan(1936, 1948, color="#159a8c", alpha=0.10, zorder=0)
    ax.text(1942, 0.04, " Antibiotics arrive\n sulfa 1935 → penicillin 1940s",
            rotation=90, ha="left", va="bottom", fontsize=7, color="#0e6b61",
            transform=ax.get_xaxis_transform(), zorder=5)


def drop_zeros(yrs, vals):
    """Log scale cannot show zeros; drop those points."""
    pairs = [(y, v) for y, v in zip(yrs, vals) if v and v > 0]
    return [y for y, _ in pairs], [v for _, v in pairs]


def cases_chart(disease, rows, case_field, title):
    yrs, cases = series(rows, case_field)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(yrs, cases, "-o", color="#c0392b", markersize=4, linewidth=1.5)
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel("Reported cases")
    tidy_linear_yaxis(ax)
    add_vaccine_lines(ax, disease)
    add_definition_marker(ax, disease)
    fig.tight_layout()
    p = os.path.join(OUT, f"{disease}_cases.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def incidence_chart(disease, rows, case_field, title, pyrs, pop):
    yrs, cases = series(rows, case_field)
    inc = [c / pop_for(y, pyrs, pop) * 100000 for y, c in zip(yrs, cases)]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(yrs, inc, "-o", color="#2c6fbb", markersize=4, linewidth=1.5)
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel("Incidence per 100,000")
    tidy_linear_yaxis(ax)
    add_vaccine_lines(ax, disease)
    add_definition_marker(ax, disease)
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
    add_definition_marker(ax, disease)
    add_treatment_marker(ax, disease)
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
        inc = [c / pop_for(y, pyrs, pop) * 100000 for y, c in zip(yrs, cases)]
        ax.plot(yrs, inc, "-o", markersize=3, linewidth=1.5,
                color=colors[disease], label=label)
    ax.set_title("Reported incidence per 100,000, U.S. — three diseases")
    ax.set_xlabel("Year")
    ax.set_ylabel("Incidence per 100,000")
    tidy_linear_yaxis(ax)
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
    add_antibiotic_band(ax)
    ax.axvline(1948, color="#888", linestyle="--", linewidth=1)
    ax.text(1948, ax.get_ylim()[1] * 0.9, " DTP routine ~1948",
            rotation=90, va="top", fontsize=8, color="#444")
    ax.set_title("Approximate death rate per 100,000, U.S., 1900-1960\n"
                 "death rates fell ~95% BEFORE vaccines — note the antibiotic era")
    ax.set_xlabel("Year")
    ax.set_ylabel("Deaths per 100,000 population")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    p = os.path.join(OUT, "early_mortality_rates.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def _cov_series(col):
    """Merge approximate historical anchors + modern NIS for one column."""
    pts = {}
    for r in read_csv("coverage_historical.csv"):
        if r[col].strip():
            pts[int(r["year"])] = (float(r[col]), True)
    for r in read_csv("coverage.csv"):
        if r[col].strip():
            pts[int(r["year"])] = (float(r[col]), False)
    yrs = sorted(pts)
    return yrs, [pts[y][0] for y in yrs], [pts[y][1] for y in yrs]


def coverage_chart():
    cols = [("measles_mmr", "#c0392b", "Measles (MMR ≥1)"),
            ("pertussis_dtap", "#e67e22", "Pertussis (DTP/DTaP ≥3)"),
            ("polio", "#27ae60", "Polio (≥3)")]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for col, color, label in cols:
        yrs, vals, approx = _cov_series(col)
        ax.plot(yrs, vals, "-o", color=color, markersize=4, label=label)
        # mark the approximate (pre-1994) anchors with hollow markers
        ax_yrs = [y for y, a in zip(yrs, approx) if a]
        ax_vals = [v for v, a in zip(vals, approx) if a]
        ax.plot(ax_yrs, ax_vals, "o", color=color, markersize=7,
                markerfacecolor="none", markeredgecolor=color)
    ax.set_ylim(0, 100)
    ax.axvspan(1950, 1994, color="#999", alpha=0.08)
    ax.text(1971, 6, "pre-1994: approx. anchors\n(hollow markers)", fontsize=8, color="#666", ha="center")
    ax.set_title("U.S. childhood vaccination coverage over time\n"
                 "(hollow = approximate historical anchors; solid = CDC NIS, 2011+)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Coverage (%)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    p = os.path.join(OUT, "coverage.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def hospitalization_chart():
    rows = read_csv("hospitalizations.csv")
    labels = [f"{r['disease']}\n{r['group']}" for r in rows]
    vals = [float(r["pct_hospitalized"]) for r in rows]
    colors = {"Measles": "#c0392b", "Pertussis": "#e67e22", "Polio": "#27ae60"}
    bar_colors = [colors[r["disease"]] for r in rows]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.bar(labels, vals, color=bar_colors)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, f"~{v:.0f}%", ha="center", fontsize=9)
    ax.set_ylim(0, 105)
    ax.set_ylabel("% of reported cases hospitalized")
    ax.set_title("Case-hospitalization proportion (documented; NOT a long-run per-100k series)\n"
                 "No national hospitalization surveillance exists back through the century")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    p = os.path.join(OUT, "hospitalization_proportion.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def polio_definition_effect():
    """Isolate the definition change using a definition-immune anchor (deaths).

    Normalize total cases, paralytic cases, and deaths to 1952 (=100). Deaths
    cannot be reclassified, so if they fall as fast as cases, the decline is real
    rather than a reporting artifact.
    """
    rows = read_csv("polio.csv")
    def col(f):
        d = {}
        for r in rows:
            v = to_int(r.get(f))
            if v is not None:
                d[int(r["year"])] = v
        return d
    total, para, deaths = col("total_cases"), col("paralytic_cases"), col("deaths")
    def norm(d):
        b = d[1952]
        return sorted((y, v / b * 100) for y, v in d.items() if 1949 <= y <= 1968 and v > 0)
    fig, ax = plt.subplots(figsize=(10.5, 6))
    for d, color, label, lw in [
        (total, "#999999", "Total reported cases (sensitive: both rules)", 1.5),
        (para, "#2c6fbb", "Paralytic cases (sensitive: 60-day rule)", 1.8),
        (deaths, "#c0392b", "Deaths — DEFINITION-IMMUNE", 2.6)]:
        pts = norm(d)
        ax.plot([y for y, _ in pts], [v for _, v in pts], "-o", color=color,
                label=label, markersize=4, linewidth=lw)
    tidy_log_yaxis(ax)
    add_definition_marker(ax, "polio")
    add_treatment_marker(ax, "polio")
    for yr, lab in [(1955, "Salk IPV"), (1961, "Sabin OPV")]:
        ax.axvline(yr, color="#555", linestyle="--", linewidth=1)
        ax.text(yr, 0.96, f" {lab} {yr}", rotation=90, va="top", fontsize=8,
                color="#444", transform=ax.get_xaxis_transform())
    ax.set_title("Polio: does the 1950s definition change explain the decline?\n"
                 "Normalized to 1952 = 100 (log scale)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Percent of 1952 level (log scale)")
    ax.legend(loc="lower left", fontsize=9)
    ax.text(0.985, 0.97,
            "Deaths can't be reclassified →\nthe decline is largely real,\nnot a definitional artifact.\nBut deaths aren't treatment-immune:\nventilation/ICU cut CFR, so deaths\nslightly OVERSTATE the drop in infections.",
            transform=ax.transAxes, ha="right", va="top", fontsize=8,
            bbox=dict(boxstyle="round", fc="#fdf2f2", ec="#c0392b", alpha=0.9))
    fig.tight_layout()
    p = os.path.join(OUT, "polio_definition_effect.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def deaths_per_100k_chart(pyrs, pop):
    cfgs = [("measles.csv", "#c0392b", "Measles", "measles_death_rate"),
            ("pertussis.csv", "#e67e22", "Pertussis", "pertussis_death_rate"),
            ("polio.csv", "#27ae60", "Polio", None)]
    early = read_csv("early_mortality_rates.csv")
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for fname, color, label, early_col in cfgs:
        rows = read_csv(fname)
        pts = {}
        for r in rows:
            d = to_int(r.get("deaths"))
            if d is not None:
                y = int(r["year"])
                pts[y] = d / pop_for(y, pyrs, pop) * 100000
        if early_col:  # backfill early-era rates
            for r in early:
                y = int(r["year"])
                if y not in pts and r[early_col].strip():
                    pts[y] = float(r[early_col])
        yrs = sorted(y for y in pts if pts[y] > 0)
        ax.plot(yrs, [pts[y] for y in yrs], "-o", color=color, markersize=4, label=label)
    ax.set_title("Deaths per 100,000 population, U.S. — three diseases (1900-present)\n"
                 "Treatment milestones (teal) lowered deaths independent of infection rates")
    ax.set_xlabel("Year")
    ax.set_ylabel("Deaths per 100,000")
    tidy_linear_yaxis(ax)
    add_antibiotic_band(ax)            # measles/pertussis: secondary-infection deaths
    ax.axvline(1952, color="#159a8c", linestyle=":", linewidth=1.6)
    ax.text(1952, 0.55, " Polio: ventilation/ICU 1952", rotation=90, ha="left",
            va="bottom", fontsize=7, color="#0e6b61", transform=ax.get_xaxis_transform())
    ax.legend()
    fig.text(0.01, 0.005,
             "Markers = years with data. Polio/measles/pertussis are annual from OWID "
             "(U.S. Public Health Reports + CDC); pre-~1920 points are decade anchors.",
             fontsize=7, color="#777")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    p = os.path.join(OUT, "deaths_per_100k.png")
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

    # New diseases (cases + deaths where the column exists)
    for key, title in [("hepb", "Hepatitis B"), ("diphtheria", "Diphtheria"),
                       ("tetanus", "Tetanus"), ("mumps", "Mumps"), ("rubella", "Rubella")]:
        rows = read_csv(f"{key}.csv")
        made.append(cases_chart(key, rows, "cases", f"{title} — reported cases, U.S."))
        made.append(deaths_chart(key, rows, f"{title} — reported deaths, U.S."))

    made.append(early_mortality_chart())
    made.append(coverage_chart())
    made.append(deaths_per_100k_chart(pyrs, pop))
    made.append(hospitalization_chart())
    made.append(polio_definition_effect())

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
