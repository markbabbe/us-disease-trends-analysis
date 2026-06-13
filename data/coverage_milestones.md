# Vaccination Coverage: Historical Milestones and Anchors

**Why this file exists.** A vaccine's *licensure year* is not the year it
protected the population. Coverage rises (sometimes slowly, sometimes in pockets)
over years to decades, and gaps in coverage explain much of the *residual*
disease and the *resurgences* seen after a vaccine exists. But there is **no
clean national annual coverage time series before ~1994**, when the CDC National
Immunization Survey (NIS) began. This file therefore gives **documented
milestones and anchor estimates with citations**, not a smooth annual series.
Modern (post-2011) machine-readable coverage is in `coverage.csv` (live from the
CDC NIS API).

> **Uncertainty note.** Pre-1994 figures below are anchor estimates from
> published CDC/MMWR historical reports; many are national approximations or
> apply to specific age groups (e.g., school entrants vs. preschoolers). Treat
> them as orders of magnitude and milestones, not precise annual coverage.

## Polio

| Year(s) | Coverage / event |
|---|---|
| Apr 1955 | Salk IPV licensed; mass child vaccination began immediately. |
| Apr–May 1955 | **Cutter incident** — defective vaccine lots caused real cases; program briefly paused, denting early confidence. |
| 1955–1960 | IPV uptake rose quickly among children and young adults; paralytic cases fell from ~21,000 (1952) to ~2,500 (1960). |
| 1961–1964 | OPV licensed; mass community campaigns ("Sabin Oral Sundays") drove rapid additional uptake. |
| late 1960s | High childhood coverage; cases fell below ~100/yr. |

**Reading:** polio uptake was *relatively fast*, so the case decline tracks
coverage closely — though the Cutter incident shows uptake was not frictionless.

## Measles

| Year(s) | Coverage / event |
|---|---|
| 1963 | Measles vaccine licensed. |
| 1966–1967 | CDC measles eradication campaign launched. |
| 1963–1968 | Reported cases fell ~90%+ (from ~400k to ~22k) — substantial but uneven uptake. |
| 1970s | States enacted **school-entry immunization laws**; by 1980 all 50 states required measles vaccine for school → school-age coverage >95%. |
| late 1980s | **Preschool (1–4 yr) coverage lagged badly** — estimated ~50–70% in some urban areas. |
| 1989–1991 | **Resurgence (~55,000 cases, 120+ deaths)** concentrated in *unvaccinated preschoolers* — a coverage-gap epidemic, not a vaccine failure. |
| 1989 | Second MMR dose recommended in response. |
| 1994 | **Vaccines for Children (VFC)** program → preschool coverage climbed to ~90%+. |

**Reading:** measles is the clearest case of your point — the vaccine existed
from 1963, but *incomplete preschool coverage* allowed large outbreaks as late
as 1989–91. Coverage, not mere availability, drove the endgame to elimination
(2000).

## Pertussis (DTP/DTaP)

| Year(s) | Coverage / event |
|---|---|
| ~1948 | Whole-cell DTP enters routine childhood use. |
| 1962 | **Vaccination Assistance Act** (Section 317) funded DTP and polio vaccination for children. |
| 1970s–1980s | DTP coverage among children high (commonly cited ≥95% ≥3 doses by school entry). |
| 1982 | "DPT: Vaccine Roulette" broadcast + whole-cell safety concerns spurred litigation and the 1986 National Childhood Vaccine Injury Act (VICP). U.S. coverage stayed relatively high. |
| 1991–1997 | Switch to **acellular DTaP** (better tolerated, but immunity wanes faster — relevant to the modern resurgence). |

## Cross-cutting policy drivers of coverage

- **1962** Vaccination Assistance Act (federal funding for childhood vaccination)
- **1970s** state school-entry immunization laws (all 50 states by ~1980)
- **1986** National Childhood Vaccine Injury Act (VICP; stabilized vaccine supply)
- **1993–1994** Vaccines for Children (VFC) program (free vaccines for eligible kids)
- **1994** National Immunization Survey (NIS) begins — first systematic national coverage measurement

## Sources

- CDC MMWR, "Achievements in Public Health, 1900–1999: Impact of Vaccines
  Universally Recommended for Children." MMWR 1999;48(12):243–248.
- CDC measles elimination and 1989–91 resurgence reports (MMWR).
- CDC, *Epidemiology and Prevention of Vaccine-Preventable Diseases* (Pink Book),
  disease-specific chapters.
- CDC National Immunization Survey (NIS) documentation, for the post-1994 era.
