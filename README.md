# Long-Term U.S. Disease Trends: Polio, Pertussis, and Measles

**An objective epidemiological and statistical analysis of disease burden over time, and of which metrics are appropriate for comparing different eras.**

> **Purpose and stance.** This document is not written to prove or disprove any
> position about vaccines. It is an attempt to assess, as neutrally as the data
> allow, *how the burden of three diseases changed across the 20th and early
> 21st centuries* and *which measurements can legitimately be compared across
> decades.* Throughout, **observed data** and **interpretation** are labeled
> separately, uncertainty is stated explicitly, and where several explanations
> are plausible they are all presented and weighed.
>
> Data are drawn primarily from U.S. government sources (CDC/MMWR, NCHS Vital
> Statistics, U.S. Census Bureau) and government-derived peer-reviewed
> compilations. Full provenance and data-quality caveats are in
> [`data/SOURCES.md`](data/SOURCES.md). Annual figures before 1950 carry
> substantial uncertainty; the **shape** of the trends is far more reliable than
> any single year's digits.
>
> **Recent years are pulled live from the CDC NNDSS open-data API** (see
> [`scripts/fetch_cdc_nndss.py`](scripts/fetch_cdc_nndss.py)). That API only
> reaches back to ~2022 and is *provisional*, so it supplements — it cannot
> replace — the historical record (which exists only as scanned MMWR annual
> summaries, the Pink Book PDF, and NCHS volumes). The live pull captures the
> **2024 pertussis resurgence (~35,500 reported)** and the **large 2025 measles
> year (~2,000+ reported, provisional)** — recent context the pre-2020
> compilation would miss.

---

## How to read this report

- **Sections 1–7** analyze each disease across the requested dimensions
  (timeline, raw cases, population-adjusted rates, age, severity, excess
  mortality, surveillance bias).
- **Section 8** argues for the most appropriate metric for cross-decade
  comparison.
- **Section 9** is the summary table and a guide to the charts.
- The final section grades every conclusion as **strongly supported**,
  **plausible but uncertain**, or **not determinable** from the data.

Charts are in [`charts/`](charts/) and are reproducible from the CSVs in
[`data/`](data/) via [`scripts/generate_charts.py`](scripts/generate_charts.py).

### A note that applies to all three diseases

The single most important methodological fact in this report:

> **A reported "case" does not mean the same thing in 1920, 1955, 1995, and
> 2020.** Case definitions, diagnostic technology, physician awareness, and
> legal reporting requirements all changed — sometimes drastically. Therefore
> raw case counts are the *least* comparable metric across eras, and severity
> metrics anchored to a fixed clinical event (death, hospitalization, paralysis
> with residual deficit) are generally *more* comparable — though they too are
> confounded by improvements in medical treatment.

---

# 1. Polio (Poliomyelitis)

## 1.1 Historical timeline

| Period | Event | Type |
|---|---|---|
| 1894 | First large reported U.S. outbreak (Rutland County, Vermont) | Outbreak |
| 1907, 1916 | Major Northeast epidemics; 1916 caused ~6,000 deaths and ~27,000 cases | Outbreak |
| 1930s–1940s | Polio becomes nationally notifiable; surveillance formalized | Surveillance |
| 1949–1954 | Enteroviruses (Coxsackie, ECHO) identified — many "nonparalytic polio" and aseptic-meningitis cases now attributable to *other* viruses | Diagnostics / case definition |
| **1952** | **Largest U.S. epidemic on record: ~57,600 cases, ~21,000 paralytic, ~3,145 deaths** | Outbreak |
| **April 1955** | **Salk inactivated polio vaccine (IPV) licensed** | Vaccine |
| Late 1950s | Paralytic-polio case definition **tightened**: required residual paralysis at follow-up (commonly ~60 days) plus clinical/lab criteria | Case definition |
| **1961–1963** | **Sabin oral polio vaccine (OPV) licensed and widely adopted** | Vaccine |
| 1979 | Last endemic wild-virus outbreak (unvaccinated Amish communities) | Outbreak |
| 1994 | Wild poliovirus declared eliminated from the Americas (PAHO/WHO) | Milestone |
| 1980s–1990s | Essentially all U.S. paralytic cases are **vaccine-associated paralytic polio (VAPP)** from OPV (~5–10/yr) | Surveillance |
| 2000 | U.S. switches to all-IPV schedule; OPV discontinued, ending VAPP | Policy |
| 2005, 2022 | Rare importations / vaccine-derived cases in undervaccinated communities | Outbreak |

## 1.2 Raw cases

*Observed (chart: [`charts/polio_cases.png`](charts/polio_cases.png)).* Reported
poliomyelitis rose through the first half of the century, peaked in 1952
(~57,600 total), and fell to single digits by the mid-1960s.

*Interpretation / caveat.* Polio raw counts are **especially treacherous** for
two reasons:

1. **The denominator of what counts as "polio" shrank.** Before the 1950s, the
   "nonparalytic poliomyelitis" category and undifferentiated aseptic meningitis
   were often labeled polio. After Coxsackie and ECHO viruses were identified
   (1949–1954), many such illnesses were correctly reclassified as *not* polio.
2. **The paralytic case definition was tightened in the late 1950s**, requiring
   documented residual paralysis. This change, by itself, reduced the number of
   illnesses meeting the "paralytic polio" bar.

Some critics argue these definitional changes manufactured part of the apparent
post-vaccine decline. **Assessment:** the reclassification and stricter
definition are real and *do* reduce the apparent drop somewhat — but they
**cannot explain the bulk of it**, because (a) the decline continued for years
after the definition stabilized, (b) the most definition-resistant endpoints —
**deaths and iron-lung/respiratory-support admissions** — fell in parallel, and
(c) the geographic pattern of decline tracked vaccine rollout. The honest
statement is: *definitional change is a genuine but partial confounder; it
shifts the magnitude, not the direction or the bulk, of the trend.*

## 1.3 Population-adjusted rates

*Observed (chart: [`charts/polio_incidence.png`](charts/polio_incidence.png)).*
At the 1952 peak, incidence was roughly **37 per 100,000**; by the mid-1960s it
was below **0.1 per 100,000**; today it is effectively zero. Because the U.S.
population more than doubled from 1916 (~100M) to 2020 (~331M), population
adjustment *widens* the apparent decline relative to raw counts — a given case
count represents a smaller share of a larger population over time.

## 1.4 Age-specific analysis

*Observed/interpretation.* Polio primarily struck **children** (hence "infantile
paralysis"), but a notable feature of the mid-century U.S. epidemics was a
**shift toward older children, adolescents, and young adults** — plausibly
because improved sanitation *delayed* first exposure past infancy, when maternal
antibody no longer protected and paralytic risk per infection is higher. This is
the well-known "hygiene paradox" of polio. **Demographic caveat:** because
attack rates and paralytic risk were strongly age-dependent, any era comparison
should ideally be age-stratified; pre-1955 surveillance rarely reported the
clean age breakdowns needed to do this rigorously.

## 1.5 Severe disease analysis

- **Mortality (most comparable):** ~3,145 deaths in 1952; ~16 by 1965;
  essentially zero thereafter (chart:
  [`charts/polio_deaths.png`](charts/polio_deaths.png)).
- **Paralysis with residual deficit:** the clinical hallmark; tracked closely
  with deaths.
- **Case fatality rate:** paralytic polio CFR was roughly **5–10%** (higher for
  bulbar disease), and itself improved with the advent of mechanical ventilation
  (the "iron lung," 1930s onward) and intensive respiratory care — i.e., *better
  treatment lowered CFR even before vaccination*, an important confounder when
  comparing severity across eras.
- **IFR:** not reliably estimable historically — the great majority of polio
  infections were asymptomatic or minor, and the asymptomatic denominator was
  never measured at population scale before serosurveys.

## 1.6 Excess / all-cause mortality

Polio deaths were never a large enough fraction of *all-cause* U.S. mortality for
excess-mortality methods to add much signal at the national level, except during
sharp localized epidemic summers. **Limitation:** all-cause mortality is too
coarse to isolate polio. Disease-specific mortality is the better tool here.

## 1.7 Surveillance bias assessment

| Factor | Direction of effect on reported polio | Magnitude |
|---|---|---|
| Underreporting (early era) | Undercount, especially of nonparalytic disease | Large but uncertain |
| Reclassification after enterovirus discovery (1949–54) | **Lowered** later counts (removed non-polio) | Moderate |
| Tightened paralytic definition (late 1950s) | **Lowered** later counts | Moderate |
| Intense public/physician awareness in epidemic years | **Raised** counts at peaks | Moderate |

**Net:** surveillance artifacts plausibly **inflate the apparent peak** and
**deflate the apparent late counts**, exaggerating the decline somewhat — but
death and paralysis data, which are far less definition-sensitive, confirm a
genuine, very large reduction.

---

# 2. Pertussis (Whooping Cough)

## 2.1 Historical timeline

| Period | Event | Type |
|---|---|---|
| Pre-1940s | Endemic with 3–4-year epidemic cycles; a leading cause of infant death | Baseline |
| ~1922 | Pertussis morbidity reporting becomes national | Surveillance |
| 1934 | Largest reported year (~265,000 cases) | Outbreak |
| **~1948** | **Whole-cell pertussis vaccine (in DTP) enters routine use** | Vaccine |
| 1976 | All-time reported low (~1,010 cases) | Milestone |
| 1980s | Resurgence begins; cyclic peaks return | Trend |
| **1991–1997** | **Switch from whole-cell (DTP) to acellular (DTaP) vaccine** (fewer side effects, but immunity wanes faster) | Vaccine |
| ~2000s | **PCR diagnosis adopted**, greatly increasing case ascertainment | Diagnostics |
| 2005 | Tdap booster recommended for adolescents/adults | Policy |
| 2010, 2012, 2014 | Large epidemic years; 2012 (~48,300) highest since 1955 | Outbreak |

## 2.2 Raw cases

*Observed (chart: [`charts/pertussis_cases.png`](charts/pertussis_cases.png)).*
Cases fell ~99% from the pre-vaccine peak (~265,000 in 1934) to the 1976 nadir
(~1,010), then **rose substantially** through the 2000s–2010s.

*Interpretation.* Pertussis is the clearest example of why raw counts mislead.
The **resurgence is partly real and partly an artifact of better detection.**
Major competing/contributing explanations (all with supporting evidence):

1. **Improved diagnostics (PCR).** PCR is far more sensitive than culture and
   detects milder/older cases that previously went unrecorded → **inflates**
   recent counts. *Strong evidence; substantial effect.*
2. **Waning immunity from the acellular (DTaP) vaccine.** Protection wanes within
   years, leaving adolescents susceptible → **genuine** increase in
   transmission. *Strong evidence.*
3. **Pathogen adaptation** (e.g., pertactin-deficient *B. pertussis* strains).
   *Moderate evidence; contributory.*
4. **Increased clinician awareness and reporting.** *Moderate.*

**Assessment:** the resurgence is best read as a *real* epidemiologic change
(waning immunity) **amplified** by a *measurement* change (PCR). Raw counts alone
cannot apportion the two; infant hospitalization and death data (below) are
needed to gauge the change in true *severe* burden.

## 2.3 Population-adjusted rates

*Observed (chart:
[`charts/pertussis_incidence.png`](charts/pertussis_incidence.png)).* Pre-vaccine
incidence reached ~150+ per 100,000; the 1976 low was ~0.5 per 100,000; modern
peaks reach ~10–15 per 100,000 — far below pre-vaccine levels but well above the
nadir. Population growth means modern raw counts understate, relative to the
past, how *uncommon* the disease has become per capita.

## 2.4 Age-specific analysis

*Observed/interpretation.* The burden is now sharply **bimodal**: most reported
cases occur in **adolescents** (waning immunity), but the most **severe disease
and nearly all deaths occur in infants <1 year**, especially <2 months (too
young to be fully vaccinated). This concentration of severe outcomes in young
infants has been **stable across eras**, which makes **infant-specific
hospitalization and mortality** the most era-comparable pertussis metrics.

## 2.5 Severe disease analysis

- **Mortality (most comparable):** pre-vaccine annual deaths numbered in the
  **thousands** (≈4,000/yr baseline per JAMA 2007; higher in the 1920s–30s);
  modern deaths are typically **~10–20/yr**, overwhelmingly infants
  (chart: [`charts/pertussis_deaths.png`](charts/pertussis_deaths.png)).
- **Hospitalizations:** concentrated in infants; the best modern severity gauge.
- **CFR:** fell dramatically across the century **independent of vaccination**
  because of supportive care (oxygen, ICU, antibiotics for secondary
  infection) — a major confounder for severity comparisons.

## 2.6 Excess / all-cause mortality

Useful mainly for the **early century**, when pertussis was a top-five cause of
infant death and thus visible in infant all-cause mortality. In the modern era
its mortality footprint is too small to detect via excess-mortality methods.

## 2.7 Surveillance bias assessment

| Factor | Direction | Magnitude |
|---|---|---|
| PCR adoption (2000s) | **Raises** recent counts | Large |
| Serology/probable-case categories | Raises recent counts | Moderate |
| Underreporting of mild/adult cases (all eras, worse early) | Undercount | Large, uncertain |
| Awareness after publicized epidemics | Raises counts | Moderate |

**Net:** recent counts are **substantially inflated by detection** relative to
mid-century — so the resurgence in *raw cases* overstates the resurgence in
*disease burden*. Infant deaths/hospitalizations show a real but far smaller
increase from the nadir.

---

# 3. Measles

## 3.1 Historical timeline

| Period | Event | Type |
|---|---|---|
| ~1912 | Measles becomes nationally notifiable | Surveillance |
| Pre-1963 | Endemic with sharp **biennial** epidemics; ~500,000 reported cases/yr but an estimated **3–4 million actual infections/yr** (near-universal childhood infection) | Baseline |
| 1958 | Largest reported postwar year (~763,000) | Outbreak |
| **1963** | **First measles vaccine (Edmonston-B) licensed**; improved further-attenuated vaccine 1968 | Vaccine |
| **1971** | **MMR combination licensed** | Vaccine |
| 1983 | Record low (~1,500 cases) | Milestone |
| **1989–1991** | **Resurgence (~55,000 cases over the period, 120+ deaths)**, concentrated in undervaccinated preschoolers | Outbreak |
| **1989** | **Second MMR dose recommended** in response | Policy |
| **2000** | **Measles declared eliminated** (no continuous endemic transmission) in the U.S. | Milestone |
| 2014, 2019 | Large import-driven outbreaks in undervaccinated communities; 2019 (~1,282) the largest post-elimination year | Outbreak |

## 3.2 Raw cases

*Observed (chart: [`charts/measles_cases.png`](charts/measles_cases.png)).*
Reported cases collapsed from hundreds of thousands per year before 1963 to
~86 at elimination (2000), with sporadic outbreak spikes since.

*Interpretation.* Two opposite biases must be stated:

1. **Pre-vaccine undercount.** Only an estimated ~10% of measles infections were
   reported (CDC). So pre-vaccine raw counts *understate* true infections by
   roughly an order of magnitude.
2. **Modern over-confirmation.** Today a "case" must meet a strict clinical
   definition **plus laboratory confirmation** (IgM, PCR, or epidemiologic link).
   Modern cases are therefore "harder" and more certain than mid-century clinical
   reports.

**Consequence:** the *true* decline in infections is even larger than raw counts
suggest (because the baseline was undercounted), but the two eras' "cases" are
not like-for-like units. Measles is clinically distinctive (so clinical
ascertainment was relatively good for a notifiable disease), which makes its raw
trend more trustworthy than pertussis's — but the order-of-magnitude
under-ascertainment of the pre-vaccine baseline is still essential context.

## 3.3 Population-adjusted rates

*Observed (chart: [`charts/measles_incidence.png`](charts/measles_incidence.png)).*
Pre-vaccine reported incidence ran **~250–500 per 100,000**; today it is a tiny
fraction of one per 100,000. Because nearly every birth cohort was infected
pre-vaccine, *true* incidence approached the **birth rate** — population growth
context matters less here than the near-universality of infection.

## 3.4 Age-specific analysis

*Observed/interpretation.* Pre-vaccine measles was a **near-universal childhood
infection** (peak ages ~5–9; most people immune by adolescence). The 1989–91
resurgence shifted into **unvaccinated preschoolers**; modern outbreaks cluster
in **undervaccinated communities** of all ages and in **infants too young to be
vaccinated**. Age structure is essential because severe outcomes
(encephalitis, death, and the rare late complication SSPE) are
age- and dose-dependent.

## 3.5 Severe disease analysis

- **Mortality (most comparable):** ~400–500 deaths/yr in the 1950s–early 1960s;
  by the 1980s, single digits to low tens; 1990 resurgence ~64; modern years
  often **0** (chart: [`charts/measles_deaths.png`](charts/measles_deaths.png)).
- **Case fatality rate:** ~**0.1–0.2%** in the mid-century U.S. (≈1–2 per 1,000
  reported cases), but **higher earlier in the century** and much higher in
  malnourished populations. The U.S. measles CFR **fell ~90% between 1900 and
  the 1950s — before any vaccine** — driven by antibiotics (for secondary
  pneumonia), nutrition, and supportive care
  (chart: [`charts/measles_cfr.png`](charts/measles_cfr.png)).
- **Other severe outcomes:** acute encephalitis (~1 per 1,000 cases),
  hospitalization, and SSPE (a fatal late complication, ~1 per several thousand
  infections, higher for infant infection).

## 3.6 Excess / all-cause mortality

The early-century **death-rate** decline (chart:
[`charts/early_mortality_rates.png`](charts/early_mortality_rates.png)) is the
most useful long-run severity signal: measles mortality per 100,000 fell from
~13 (1900) to ~0.3 (1950) **before** the vaccine, then the vaccine drove
*incidence* — and thus the remaining deaths — toward zero. **Limitation:**
early death rates come from the partial Death Registration Area and are
approximate; treat the *shape*, not the digits, as evidence.

## 3.7 Surveillance bias assessment

| Factor | Direction | Magnitude |
|---|---|---|
| Pre-vaccine under-ascertainment (~10% reported) | **Understates** baseline infections | Large (~10×) |
| Modern lab-confirmation requirement | Makes modern cases "harder"/fewer | Moderate |
| High clinical recognizability of measles | Improves ascertainment in all eras | Stabilizing |

**Net:** unlike pertussis, measles biases mostly **understate the pre-vaccine
baseline**, so the true decline in infections is *larger* than the raw-count
decline — the opposite direction of the pertussis artifact.

---

# 8. Which metric is best for long-term comparison?

**Recommendation, by purpose:**

| Comparison goal | Best metric | Why |
|---|---|---|
| **Did severe disease burden change?** | **Mortality and (where available) hospitalization rates per 100,000**, ideally age-specific | Anchored to fixed clinical events that are least sensitive to changing case definitions and test technology. Best single choice for cross-decade comparison. |
| Did *transmission/infection* change? | **Incidence per 100,000**, with explicit ascertainment caveats | Population-adjusted, but only trustworthy when case definition and detection are stable. |
| Cross-disease or cross-era *severity* | **Case fatality rate**, *with* a treatment-era caveat | Reveals how lethal the disease was per case — but improvements in care lower CFR independent of incidence, so it conflates virulence with medicine. |
| Headline/communication only | Raw cases | Intuitive but the **least comparable** across eras; avoid for inference. |

**Justification.** Across all three diseases, the recurring problem is that *what
counts as a case changed* — through enterovirus reclassification and the
tightened paralytic definition (polio), PCR adoption and acellular-vaccine
dynamics (pertussis), and the shift from clinical to lab-confirmed diagnosis
(measles). Metrics tied to a **fixed, severe, hard-to-misclassify endpoint**
(death; paralysis with residual deficit; infant hospitalization) are therefore
the most defensible for long-term comparison.

**The essential caveat that cuts the other way:** mortality and CFR are **lowered
by medical progress independent of incidence.** Mechanical ventilation (polio),
ICU/antibiotics/oxygen (pertussis, measles pneumonia), and better nutrition all
reduced deaths-per-case *before and during* the vaccine era. So **falling deaths
overstate the decline in *infection*, while falling cases (for pertussis)
overstate the decline in true *burden* and (for measles) understate the historic
baseline.** No single metric is clean; the honest approach is to **triangulate**:
read incidence, mortality, and CFR together, each with its known bias.

The best practical summary metric for "how much did this disease hurt people, and
how did that change" is **age-specific mortality/hospitalization rate per
100,000**, interpreted alongside incidence and with an explicit note on
medical-treatment improvements.

---

# 8b. Vaccine availability vs. coverage — a necessary companion metric

Incidence and mortality trends cannot be interpreted correctly using a vaccine's
**licensure year** alone. What protects a population is **coverage**, which rises
over years to decades and is often uneven across age groups and communities.
Coverage gaps explain much of the *residual* disease and the *resurgences* that
occur even after a vaccine exists.

*Observed (chart: [`charts/coverage.png`](charts/coverage.png); live data:
[`data/coverage.csv`](data/coverage.csv) from the CDC NIS API).* Modern U.S.
childhood coverage by age 24 months sits on a plateau of roughly **80–93%**
(MMR ≥1 dose ~90%, polio ~92%, DTaP ≥4 doses ~81%).

**The key limitation, stated plainly:** there is **no clean national annual
coverage series before ~1994**, when the CDC National Immunization Survey began.
The most decision-relevant period for the "availability ≠ protection" question —
the early uptake decades (polio 1955+, measles 1963+) — is therefore documented
as **cited milestones and anchor estimates**, not a continuous series. Full
detail and sources: [`data/coverage_milestones.md`](data/coverage_milestones.md).
Highlights:

- **Polio:** uptake was relatively fast after 1955, so the case decline tracks
  coverage closely — though the 1955 **Cutter incident** shows it was not
  frictionless.
- **Measles:** the clearest illustration of the point. The vaccine existed from
  1963, but **incomplete preschool coverage** (estimated ~50–70% in some urban
  areas in the late 1980s) allowed the **1989–91 resurgence (~55,000 cases)**
  among unvaccinated preschoolers. School-entry laws (1970s), the second dose
  (1989), and Vaccines for Children (1994) closed the gap and drove elimination
  (2000).
- **Pertussis:** high childhood DTP coverage from the 1960s–80s; the modern
  resurgence is tied less to *coverage* than to **waning acellular-vaccine
  immunity** plus **PCR detection** (§2).

**Interpretive consequence:** when a case trend does *not* fall immediately after
a vaccine's licensure (measles in the 1960s–80s; pertussis recently), the
explanation is usually found in **coverage and vaccine-type dynamics**, not in
the vaccine's mere existence. Coverage is thus an essential companion to any
incidence comparison across the post-licensure era.

# 9. Summary

## 9.1 Summary table

| Disease | Best metric for long-term comparison | Trend **before** vaccine era | Trend **after** vaccine era | Major caveats |
|---|---|---|---|---|
| **Polio** | Deaths & paralytic cases per 100,000 (age-specific ideal) | Rising, with severe epidemic peaks (1952: ~57.6k cases, ~3,145 deaths) | Fell >99% within a decade; wild virus eliminated by 1979; deaths ≈0 | Late-1950s definition tightening + enterovirus reclassification deflate later counts; ventilator care lowered CFR pre-vaccine; asymptomatic denominator never measured |
| **Pertussis** | Infant mortality & hospitalization rate | Very high (~265k cases 1934; thousands of deaths/yr) | Fell ~99% to 1976 nadir, then **partial resurgence** in cases | Resurgence inflated by PCR detection; waning acellular immunity is real; deaths now ~10–20/yr, mostly infants; CFR fell via supportive care |
| **Measles** | Deaths per 100,000 + incidence (with ascertainment caveat) | Near-universal childhood infection (~3–4M true infections/yr); deaths declining for decades | Cases fell ~99%+; eliminated 2000; outbreaks since via undervaccination | Pre-vaccine cases undercounted ~10×; modern cases lab-confirmed; CFR fell ~90% (1900→1950) before vaccine |

## 9.2 Charts

| Chart | File |
|---|---|
| Combined incidence per 100,000 (all three) | [`charts/combined_incidence.png`](charts/combined_incidence.png) |
| Early-century death rates 1900–1960 (measles, pertussis) | [`charts/early_mortality_rates.png`](charts/early_mortality_rates.png) |
| Childhood vaccination coverage (CDC NIS, 2011+) | [`charts/coverage.png`](charts/coverage.png) |
| Polio — cases / incidence / deaths | [`charts/polio_cases.png`](charts/polio_cases.png) · [`charts/polio_incidence.png`](charts/polio_incidence.png) · [`charts/polio_deaths.png`](charts/polio_deaths.png) |
| Pertussis — cases / incidence / deaths | [`charts/pertussis_cases.png`](charts/pertussis_cases.png) · [`charts/pertussis_incidence.png`](charts/pertussis_incidence.png) · [`charts/pertussis_deaths.png`](charts/pertussis_deaths.png) |
| Measles — cases / incidence / deaths / CFR | [`charts/measles_cases.png`](charts/measles_cases.png) · [`charts/measles_incidence.png`](charts/measles_incidence.png) · [`charts/measles_deaths.png`](charts/measles_deaths.png) · [`charts/measles_cfr.png`](charts/measles_cfr.png) |

---

# What the evidence does and does not support

### Strongly supported by the evidence

- **Reported incidence (cases per 100,000) of all three diseases fell
  dramatically over the 20th century**, with the steepest, fastest declines
  beginning at or shortly after each vaccine's introduction (polio after 1955/61,
  measles after 1963, pertussis after the late 1940s). The magnitude is large
  enough to survive plausible surveillance-bias corrections.
- **Deaths from all three diseases fell to near zero** by the late 20th century.
  Because mortality is the metric least sensitive to changing case definitions,
  this is the most robust single finding.
- **Wild poliovirus transmission and endemic measles transmission were
  eliminated in the U.S.** (1979 and 2000 respectively) — discrete, well-
  documented events.
- **Case fatality fell substantially *before* vaccines** for measles and
  pertussis, driven by antibiotics, nutrition, and supportive/critical care.
  Medical progress is a genuine, independent contributor to falling deaths.
- **Raw case counts are not comparable across eras** for any of the three
  diseases, because case definitions and diagnostics changed materially.

### Plausible but uncertain

- **The exact share of the polio "decline" attributable to definitional/
  diagnostic reclassification** versus true reduction. Reclassification is real
  and partial; the weight of evidence (parallel decline in deaths and
  ventilator use, geographic tracking with vaccination) indicates it is a minor
  fraction of the total, but a precise decomposition is not available.
- **How much of the modern pertussis resurgence is "real" (waning immunity,
  strain change) versus "detected" (PCR).** Both are well supported; their exact
  ratio is not pinned down by the available aggregate data.
- **Pre-vaccine true infection counts** (especially measles ~3–4M/yr and the
  pertussis baseline). These are model/serology-based estimates with wide bands,
  not direct counts.

### Cannot be determined from the available data

- **Precise infection fatality rates (IFR) for any of the three across most of
  the century**, because the asymptomatic/mild infection denominator was never
  measured at population scale before modern serosurveys.
- **A clean attribution of *each* year's change to a single cause.** Vaccination,
  medical care, sanitation, nutrition, demographic shifts, and surveillance
  changes overlap in time; aggregate national data cannot uniquely partition
  their contributions year by year.
- **Whether early-century (pre-1933) absolute case and death *counts* are
  accurate to within a small margin** — Death Registration Area coverage was
  partial and morbidity reporting immature, so only trend shape, not precise
  early values, can be relied upon.

---

*Compiled as an objective epidemiological/statistical analysis. Sources and
data-quality notes: [`data/SOURCES.md`](data/SOURCES.md). All figures are
reproducible from the CSVs and script in this repository. Where this document
states a number, treat the **trend** as the finding and the **digits** —
especially pre-1950 — as approximate.*
