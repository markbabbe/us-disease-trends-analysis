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
- **Our World in Data — U.S. polio case-rate and death-rate series (1910–2023).**
  Used to build the complete annual polio series. OWID's underlying sources are
  U.S. Public Health Reports (1942) and the CDC; population from various sources.
  https://ourworldindata.org/polio

## File-by-file notes

- `us_population.csv` — Decennial census counts; 2024 is a Census estimate.
- `measles.csv` — **Complete annual series, 1919–2025**, rebuilt by
  [`scripts/build_measles_pertussis_from_owid.py`](../scripts/build_measles_pertussis_from_owid.py)
  from OWID (`owid_combined_cases.csv` for case counts, `owid_measles_rate.csv`
  death rate × Census population for deaths; underlying U.S. Public Health
  Reports + CDC). **Known gap: OWID lacks measles case counts for 1926–1937**
  (deaths are present), so the cases chart interpolates across that window —
  markers show where real data exists. CDC estimates pre-vaccine reported cases
  (~500k/yr) were a fraction of an estimated 3–4 million actual infections/yr.
- `polio.csv` — **Complete annual series, 1910–1971**, rebuilt by
  [`scripts/build_polio_from_owid.py`](../scripts/build_polio_from_owid.py) from
  `polio_owid_rates.csv` (Our World in Data's U.S. polio death-rate and case-rate
  series; underlying sources: **U.S. Public Health Reports (1942) and the CDC**,
  processed by OWID), converted to counts using interpolated Census population.
  "paralytic_cases" are retained from the prior CDC-anchored compilation where
  available (dropped in the few late years where source rounding put them above
  the annual total). Post-1971 rows (1979, 1990, 2000, 2005, 2022) are kept as
  documented specific events rather than annual rates. The case definition for
  paralytic polio was tightened in the late 1950s (see report §1, §7).
  *Earlier versions used sparse anchor years; this rebuild eliminates the long
  straight-line interpolations (e.g., the former 1916→1949 gap in deaths).*
- `polio_owid_rates.csv` — raw download of the OWID U.S. polio death-rate and
  case-rate series (per 100,000), 1910–2023. Source as above.

### Chart scale

Static charts use a **linear** y-axis (from 0) so the absolute drop-off is
visible at true scale. The trade-off: values far below the peak (modern
resurgences, the long low tail) compress toward the axis and are hard to read.
The interactive dashboard has a **log/linear toggle** for when you need to see
those small values; the static incidence/deaths charts favor the linear view of
the decline. (The polio definition-effect chart stays on a log axis because its
argument is about *proportional* tracking — equal ratios as equal distances.)
- `pertussis.csv` — **Complete annual series, 1922–2025** (cases) and 1944–2022
  (deaths), rebuilt from OWID `owid_pertussis.csv` (U.S. Public Health Reports +
  CDC); 2023–2025 cases appended from CDC NNDSS (provisional, captures the 2024
  resurgence). Pre-1930 death *rates* remain in `early_mortality_rates.csv`.
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

## Additional diseases (DTaP, HepB, MMR tabs)

- `diphtheria.csv`, `mumps.csv`, `rubella.csv` — built by
  [`scripts/build_new_diseases.py`](../scripts/build_new_diseases.py) from saved
  OWID raw files (`owid_diphtheria.csv`, `owid_mumps.csv`, `owid_rubella.csv`;
  OWID's underlying sources are U.S. Public Health Reports + CDC). Series start
  where the disease became reportable / data exists: **diphtheria 1937**
  (>100k cases/yr in the 1920s predate the series), **mumps 1968** (vaccine
  1967), **rubella 1966** (vaccine 1969). Rubella's main harm is congenital
  rubella syndrome (birth defects), not deaths, so no death series is shown.
- `tetanus.csv` — annual 2009–2023 from **CDC MMWR Tetanus Surveillance
  (SS-7501, 2009–2023)**; pre-2009 are approximate anchors (1947 ~560 cases at
  3.9/million; "50–100/yr since the mid-1970s"; 2001–2008 averaged 29/yr).
  Tetanus is **not contagious** (environmental spores), so herd immunity does
  not apply — included because it is part of DTaP.
- `hepb.csv` — reported **acute** hepatitis B cases (CDC MMWR / Viral Hepatitis
  Surveillance): 1985 peak 26,654; 1990 21,102; 2002 8,064; 2010 3,350; 2020
  2,157 (1980 approximate). Reportable only from ~1966; vaccine 1981, infant/
  universal 1991. Acute-case surveillance **misses chronic infection** and the
  later cirrhosis/liver-cancer deaths it causes, and undercounts true infections
  (~6–10×).

## Childhood meningitis death rate (Hib proxy) — NCHS HIST001R

`childhood_meningitis_death_rates.csv` is transcribed from **NCHS Table HIST001R**
("Death rates by 10-year age groups and age-adjusted death rates for 113 selected
causes, United States, 1979–1998," ICD-9), cause **Meningitis (320–322)**, all
races/both sexes. `https://www.cdc.gov/nchs/data/statab/hist001r.pdf` (p. 287).

Why it's here: **Hib-specific deaths are not in standard U.S. mortality tables** —
that 113-cause list has no Haemophilus line; Hib deaths were coded under
meningitis/septicemia. Since Hib was the leading cause of childhood bacterial
meningitis pre-vaccine, the childhood meningitis death rate is the best available
mortality proxy. The 1–4-year rate fell from ~1.0/100,000 (1987) to ~0.2 after
the 1990 infant Hib vaccine. Caveat: all-cause meningitis, so it overstates Hib's
share; the under-1 pre-1990 decline largely reflects improved treatment.

The same table confirms that **measles, pertussis, and polio death rates were
already below the reportable threshold (shown as "*") by 1979** — i.e.,
near-eliminated as causes of death by then.

## Hib, PCV, Rotavirus (recent-vaccine diseases — anchor-based)

These three lack long annual notifiable-case series; their burden is measured
differently and mostly recently, so the CSVs are **documented anchors with clear
"what's measured" notes**, not annual counts:

- `hib.csv` — invasive **Haemophilus influenzae type b** disease in children <5.
  Pre-vaccine ~20,000 cases/yr and ~1,000 deaths (CDC/Roush 2007); conjugate
  vaccine 1987–1990 → >99% decline (18 cases in <5 in 2019). The 1987 anchor uses
  CDC's measured baseline (~41/100,000 <5); **1980 and 1985 are a pre-vaccine
  plateau estimate** at that surveillance level (no granular early-1980s annual
  data is published). Rate is per 100,000 children <5 (see under-5 denominator
  below). Intermediate points approximate.
- `pcv.csv` — invasive **pneumococcal** disease in children <5 (CDC Active
  Bacterial Core surveillance): 15,707 (1997) → 1,382 (2019), −91%. PCV7 2000,
  PCV13 2010. (Pneumococcus also heavily affects older adults — not shown.)
- `rotavirus.csv` — this series is **hospitalizations** in children <5, not
  reported cases (rotavirus has no long notifiable record). Pre-vaccine
  ~55,000–70,000 hospitalizations and 20–60 deaths/yr; vaccine 2006 → large
  declines. Intermediate points approximate.

Because these count disease **in children <5**, the dashboard's "per 100,000"
(which uses total U.S. population) understates the true childhood rate — read the
**counts**, and see each disease's facts.

## Chronic illness tab (`chronic_illness.csv`) — read the caveats

This tab plots three chronic conditions over time next to the **count of diseases
on the routine childhood/adolescent immunization schedule**. It exists to show the
data honestly, **not** to imply a causal link — the evidence is firmly against one.

- **Autism** — CDC Autism and Developmental Disabilities Monitoring (ADDM)
  network, identified prevalence among 8-year-olds, surveillance years 2000–2022
  (6.7 → 32.2 per 1,000; "1 in 150" → "1 in 31").
- **Asthma** — NHIS current childhood asthma prevalence, ~1980–2019. A 1997 NHIS
  redesign breaks pre/post comparability.
- **Eczema** — atopic dermatitis in children; **approximate** anchors (no clean
  long U.S. annual series; literature reports a ~2–3× rise since the 1970s to
  ~10–13% today).
- **Vaccine count** — number of *diseases* protected against on the routine
  schedule (definition-dependent; antigen/dose counts differ).

**Why correlation here is not evidence of causation:**
1. **Data can't reach 1950.** Autism wasn't a distinct diagnosis until 1980
   (DSM-III) or systematically measured until ~2000; asthma starts ~1980. Only
   the vaccine count spans the full period.
2. **The autism rise is largely ascertainment**: broadened criteria
   (DSM-III 1980 → DSM-IV 1994 spectrum/Asperger → DSM-5 2013), diagnostic
   substitution, awareness, screening, and service eligibility.
3. **Asthma/eczema** rises are studied via the hygiene hypothesis, environment,
   obesity, and urbanization.
4. **Vaccines specifically have been tested and found NOT associated with
   autism**: Hviid et al., Ann Intern Med 2019 (657,461 children); DeStefano et
   al., J Pediatr 2013 (antigen number/timing); Madsen et al., NEJM 2002; U.S.
   Institute of Medicine reviews (2004, 2011); Cochrane review. The 1998
   Wakefield paper alleging an MMR–autism link was **retracted for fraud**.

So shared upward time-trends reflect **confounding by secular trends**, the
classic correlation-not-causation pitfall this whole project is built to avoid.

## Deaths per 100,000 over time

Computed in `scripts/build_dashboard_data.py` and `generate_charts.py` as death
count ÷ interpolated Census population × 100,000. Early measles/pertussis points
(1900–1930) use the approximate Death Registration Area rates in
`early_mortality_rates.csv`; later points are derived from the death counts in
the disease CSVs. This is the recommended long-run severity metric.

## Treatment milestones (`treatment_milestones.md`)

Documents *where and when* medical treatment improved (iron lung 1928; positive-
pressure ventilation / first ICU, Copenhagen 1952; antibiotics — sulfa 1935,
penicillin 1940s; infant intensive care from the 1960s) and the effect on
case-fatality. These are marked in teal on the deaths charts. Adoption dates are
approximate (technologies diffused over years). This matters because a falling
death rate can reflect better care, not only less disease.

## Hospitalizations (`hospitalizations.csv`)

**There is no continuous national hospitalization rate for these diseases across
the century.** The earliest systematic sources — NCHS National Hospital
Discharge Survey (1965+) and HCUP (1988+) — are modern. `hospitalizations.csv`
therefore records the **documented case-hospitalization proportion** (% of
reported cases hospitalized) by era, from CDC surveillance, not a per-100,000
time series. See README §7b.

## Vaccination coverage (live CDC NIS API)

`coverage.csv` is pulled live from the CDC National Immunization Survey via
[`scripts/fetch_cdc_coverage.py`](../scripts/fetch_cdc_coverage.py):

- **Endpoint:** `https://data.cdc.gov/resource/fhky-rtsk.json` — "Vaccination
  Coverage among Young Children (0-35 Months)."
- **Metrics:** MMR ≥1 dose, DTaP ≥4 doses, polio ≥3 doses, by age 24 months,
  national, "Overall" by birth year.
- **Limit:** this dataset begins ~birth-year 2011; the NIS itself started 1994.
  There is **no clean national annual coverage series before ~1994** — the
  early-uptake decades are documented as milestones in `coverage_milestones.md`
  (from published CDC/MMWR historical reports), not as an API series.

See `coverage_milestones.md` for the historical coverage narrative and the
"availability ≠ coverage" discussion.

## Reproducing the charts

```
python3 -m venv .venv && .venv/bin/pip install matplotlib numpy
.venv/bin/python scripts/generate_charts.py
```
