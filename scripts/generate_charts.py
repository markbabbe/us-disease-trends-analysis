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
    "rotavirus": [(2006, "Rotavirus vaccine")],
    "hib": [(1990, "Hib conjugate")],
    "pcv": [(2000, "PCV7"), (2010, "PCV13")],
    "diphtheria": [(1948, "DTP")],
    "tetanus": [(1948, "DTP (toxoid)")],
    "mumps": [(1967, "Mumps vaccine"), (1971, "MMR")],
    "rubella": [(1969, "Rubella vaccine"), (1971, "MMR")],
}


def _partial_years():
    """{csv filename -> {years}} for rows that are an INCOMPLETE current year.

    The static PNGs are the complete-year archive: a year-to-date row plotted as an
    annual total would read as a real collapse, so those rows are dropped here. The
    interactive dashboard keeps them and draws them explicitly marked as partial.
    """
    out = {}
    path = os.path.join(DATA, "partial_years.csv")
    if not os.path.exists(path):
        return out
    with open(path) as f:
        for r in csv.DictReader(f):
            out.setdefault(r["disease"] + ".csv", set()).add(int(r["year"]))
    return out


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        rows = list(csv.DictReader(f))
    drop = _partial_years().get(name, set())
    return [r for r in rows if int(r["year"]) not in drop] if drop else rows


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
            pts.append((int(r["year"]), d / c * 100, c))
    if len(pts) < 2:
        return None
    pts.sort()
    yrs = [y for y, _, _ in pts]
    cfr = [v for _, v, _ in pts]
    counts = [c for _, _, c in pts]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(yrs, cfr, "-o", color="#8e44ad", markersize=4, linewidth=1.5)
    # Deaths / REPORTED cases. Early reporting captured a small and rapidly
    # changing share of infections (~10% for pre-vaccine measles), so the early
    # points measure the denominator's incompleteness as much as lethality.
    # Draw them hollow so the level isn't read as a true case-fatality rate.
    # Two distinct denominator problems, both marked hollow:
    #   early years  — only a small, fast-changing share of infections was reported
    #   small-n years — a modern year with 55 reported cases turns 2 deaths into 3.6%
    MIN_N = 500
    weak = [(y, v) for y, v, c in pts if y < 1930 or c < MIN_N]
    if weak:
        ax.plot([y for y, _ in weak], [v for _, v in weak], "o", markersize=8,
                markerfacecolor="none", markeredgecolor="#8e44ad", markeredgewidth=1.4)
        peak = max(weak, key=lambda t: t[1])
        ax.annotate("HOLLOW = don't read as lethality.\n"
                    "Early years: only ~10% of infections were reported, so the\n"
                    "denominator is missing (1919 reads 7.4%).\n"
                    f"Recent years: fewer than {MIN_N} reported cases, so one or two\n"
                    "deaths swing the ratio by whole percentage points.",
                    xy=(peak[0], peak[1]), xytext=(0.34, 0.86),
                    textcoords="axes fraction", fontsize=8, color="#5b2c6f",
                    arrowprops=dict(arrowstyle="->", color="#8e44ad", lw=1),
                    bbox=dict(boxstyle="round", fc="#f6eefb", ec="#8e44ad", alpha=0.95))
    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel("Deaths per 100 REPORTED cases (%)")
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


def _break_gaps(yrs, vals, max_gap=1):
    """Insert a NaN wherever the series skips years, so the line breaks instead of
    drawing a straight segment across missing data (Appendix E has no 1986-1990)."""
    oy, ov = [], []
    for i, (y, v) in enumerate(zip(yrs, vals)):
        if i and y - yrs[i - 1] > max_gap:
            oy.append(yrs[i - 1] + 0.5)
            ov.append(float("nan"))
        oy.append(y)
        ov.append(v)
    return oy, ov


def _pinkbook_series(col):
    """Measured annual coverage from CDC Pink Book Appendix E (1962-2016)."""
    pts = []
    for r in read_csv("coverage_levels_pinkbook.csv"):
        v = (r.get(col) or "").strip()
        if v:
            pts.append((int(r["year"]), float(v)))
    return _break_gaps([y for y, _ in pts], [v for _, v in pts])


def _nis_series(col):
    """Live CDC NIS series (coverage.csv), indexed by BIRTH year."""
    pts = []
    for r in read_csv("coverage.csv"):
        v = (r.get(col) or "").strip()
        if v:
            pts.append((int(r["year"]), float(v)))
    return [y for y, _ in pts], [v for _, v in pts]


def coverage_chart():
    """Measured coverage only.

    This chart used to splice in `coverage_historical.csv` — unsourced pre-1994
    "approx" anchors that disagreed with the measured Pink Book series by up to
    19 points (1991 polio: 72 vs 53.2). Those anchors are gone. What is plotted
    now is measured data from two surveys whose x-axes mean different things, so
    they are drawn as separate lines rather than joined into one.
    """
    cols = [("mmr", "measles_mmr", "#c0392b", "Measles (MMR ≥1)"),
            ("dtp3", "pertussis_dtap", "#e67e22", "Pertussis (DTP/DTaP ≥3)"),
            ("polio3", "polio", "#27ae60", "Polio (≥3)")]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for pb_col, nis_col, color, label in cols:
        yrs, vals = _pinkbook_series(pb_col)
        ax.plot(yrs, vals, "-o", color=color, markersize=3.5, linewidth=1.6,
                label=f"{label} — Pink Book App. E (survey year)")
        nyrs, nvals = _nis_series(nis_col)
        ax.plot(nyrs, nvals, "--s", color=color, markersize=3.5, linewidth=1.4,
                alpha=0.75, label=f"{label} — CDC NIS (birth year)")
    ax.set_ylim(0, 100)
    ax.set_title("U.S. childhood vaccination coverage, measured sources only\n"
                 "Pink Book Appendix E 1962-2016 (solid) · CDC NIS by birth year (dashed)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Coverage (%)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right", fontsize=7.5, ncol=2, framealpha=0.95)
    ax.text(0.015, 0.90,
            "Two measured surveys, indexed differently (survey year vs birth year,\n"
            "~2-year offset) — plotted separately, not spliced. Line breaks = years\n"
            "Appendix E does not report (1986-1990).",
            transform=ax.transAxes, fontsize=7.5, color="#555", va="top",
            bbox=dict(boxstyle="round", fc="#f4f4f4", ec="#bbb", alpha=0.9))
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


def childhood_meningitis_chart():
    """Childhood meningitis death rate (a Hib proxy) — NCHS HIST001R, 1979-1998."""
    rows = read_csv("childhood_meningitis_death_rates.csv")
    yrs = [int(r["year"]) for r in rows]
    u1 = [float(r["under1"]) for r in rows]
    a14 = [float(r["age1_4"]) for r in rows]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(yrs, u1, "-o", color="#bb8fce", markersize=4, label="Under 1 year")
    ax.plot(yrs, a14, "-o", color="#27ae60", markersize=4, label="1-4 years")
    ax.axvline(1990, color="#159a8c", linestyle=":", linewidth=1.6)
    ax.text(1990, 0.93, " Hib infant vaccine 1990", rotation=90, va="top",
            fontsize=8, color="#0e6b61", transform=ax.get_xaxis_transform())
    ax.set_ylim(bottom=0)
    ax.set_title("Childhood meningitis death rate, U.S., 1979-1998 (a Hib proxy)\n"
                 "All-cause meningitis (NCHS); Hib was the top cause in young children pre-vaccine")
    ax.set_xlabel("Year")
    ax.set_ylabel("Deaths per 100,000 (age group)")
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.text(0.01, 0.005,
             "Under-1 decline pre-1990 reflects better meningitis treatment; the 1-4yr drop "
             "after the 1990 Hib vaccine is the cleaner Hib signal. Source: NCHS Table HIST001R.",
             fontsize=7, color="#777")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    p = os.path.join(OUT, "childhood_meningitis.png")
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
    for key, title, field in [("hepb", "Hepatitis B", "cases"),
                              ("rotavirus", "Rotavirus (hospitalizations)", "hospitalizations"),
                              ("diphtheria", "Diphtheria", "cases"), ("tetanus", "Tetanus", "cases"),
                              ("hib", "Hib (invasive, <5)", "cases"),
                              ("pcv", "Pneumococcal (invasive, <5)", "cases"),
                              ("mumps", "Mumps", "cases"), ("rubella", "Rubella", "cases")]:
        rows = read_csv(f"{key}.csv")
        made.append(cases_chart(key, rows, field, f"{title} — U.S."))
        made.append(deaths_chart(key, rows, f"{title} — reported deaths, U.S."))

    made.append(early_mortality_chart())
    made.append(coverage_chart())
    made.append(deaths_per_100k_chart(pyrs, pop))
    made.append(hospitalization_chart())
    made.append(childhood_meningitis_chart())
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
