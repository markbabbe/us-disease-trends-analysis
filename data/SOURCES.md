# Data Sources and Provenance

This analysis prioritizes U.S. government and government-derived sources. Where a
specific annual figure is approximate or digitized from a published chart, it is
labeled as such. The **shape** of the long-term trends is robust; individual
annual digits — especially before 1950 — carry real uncertainty.

## Primary sources

- **CDC, MMWR — Summary of Notifiable Diseases, United States** (annual). The
  authoritative running record of nationally reported case counts.
  https://www.cdc.gov/mmwr/mmwr_nd/index.html
- **CDC, *Epidemiology and Prevention of Vaccine-Preventable Diseases* ("Pink
  Book"), Appendix E — Reported Cases and Deaths.** Compiles historical annual
  case and death counts for vaccine-preventable diseases.
  https://www.cdc.gov/vaccines/pubs/pinkbook/
- **CDC, MMWR. "Achievements in Public Health, 1900–1999: Control of Infectious
  Diseases." MMWR 1999;48(29):621–629.** Source for the long mortality decline
  and the role of non-vaccine factors (sanitation, antibiotics, nutrition).
- **Roush SW, Murphy TV, et al. "Historical Comparisons of Morbidity and
  Mortality for Vaccine-Preventable Diseases in the United States." JAMA
  2007;298(18):2155–2163.** Source for the pre-vaccine 20th-century annual
  baseline averages used in this report.
- **NCHS / National Vital Statistics System** (and its predecessor the Death
  Registration Area). Source for cause-specific mortality. The Death
  Registration Area covered only ~10 states (~26% of the U.S. population) in
  1900 and did not include all states until 1933 — a key early-century caveat.
- **U.S. Census Bureau.** Decennial census counts (1900–2020) and Vintage 2024
  population estimate, used as denominators for per-100,000 rates. See
  `us_population.csv`.
- **CDC measles, pertussis, and polio surveillance pages and outbreak reports**
  for the post-elimination era and modern case definitions.

## File-by-file notes

- `us_population.csv` — Decennial census counts; 2024 is a Census estimate.
- `measles.csv` — Reported cases from CDC MMWR/Pink Book; deaths from NCHS.
  Pre-1950 figures are less complete. CDC estimates that pre-vaccine reported
  cases (~500k/yr) represented only a fraction of an estimated 3–4 million
  actual infections per year.
- `polio.csv` — "total_cases" = all reported poliomyelitis; "paralytic_cases"
  reported where available. The 1916 row is an approximate national figure for
  the Northeast-centered epidemic. The case definition for paralytic polio was
  tightened in the late 1950s (see report §1, §7).
- `pertussis.csv` — Reported cases from CDC MMWR/Pink Book; deaths from NCHS.
  PCR-based diagnosis expanded ascertainment in the 2000s (see report §7).
- `early_mortality_rates.csv` — **Approximate** death rates per 100,000,
  digitized/rounded from published NCHS/Historical Statistics mortality-decline
  series. Use for trend shape, not precise values. Early years reflect partial
  Death Registration Area coverage.

## Live CDC API connection (recent years)

Recent national counts (2022–present) are pulled **live** from the CDC NNDSS
open-data API and saved to `cdc_nndss_recent.csv` by
[`scripts/fetch_cdc_nndss.py`](../scripts/fetch_cdc_nndss.py):

- **Endpoint:** `https://data.cdc.gov/resource/x9gk-5huc.json` (Socrata API
  behind the MMWR weekly notifiable-disease tables, "NNDSS Weekly Data").
- **Method:** sum the year-end cumulative column (`m3`) across sub-labels
  (e.g., "Measles, Imported" + "Measles, Indigenous"), restricted to
  `states = Total` to avoid double-counting state/region/national rows.

**What the CDC API can and cannot do — important:**

- ✅ It provides authoritative *recent* national surveillance counts. Validation:
  the API returns measles 2022 = 122, matching the finalized MMWR figure (~121).
- ⚠️ It is **weekly provisional** data. Provisional cumulative counts can differ
  a few percent from the finalized MMWR annual summary, and the current year is
  partial (excluded from the trend charts).
- ❌ It does **not** contain the deep historical series (1900–2020) this project
  depends on. The consolidated weekly dataset only goes back to ~2022. The
  long historical record exists only as **scanned MMWR annual summaries, the
  Pink Book Appendix E (PDF), and NCHS Vital Statistics volumes** — none of
  which is exposed as a clean time-series API. (The closest machine-readable
  digitization of the historical U.S. record is the academic *Project Tycho*
  dataset, derived from these same U.S. government reports.)

The 2022–2025 rows in `measles.csv` and `pertussis.csv` are therefore labeled as
CDC NNDSS API (provisional). They capture the recent measles resurgence (2025)
and pertussis resurgence (2024) that the historical compilation alone would miss.

## Reproducing the charts

```
python3 -m venv .venv && .venv/bin/pip install matplotlib numpy
.venv/bin/python scripts/generate_charts.py
```
