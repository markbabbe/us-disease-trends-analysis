# Treatment Milestones — why case-fatality fell partly independent of vaccines

Deaths from these diseases fell not only because fewer people were infected
(vaccines, and for polio some epidemic variation) but because **the same illness
became more survivable**. This file records *where and when* medical treatment
improved, because that timing matters for interpreting the death curves: a
falling death rate can reflect better care, not only less disease.

> **Uncertainty note.** Exact "widespread adoption" dates are approximate —
> technologies and drugs diffused over years and unevenly by region and hospital.
> The milestones and their direction of effect are well documented; the precise
> year a given hospital benefited is not.

## Polio — mechanical ventilation and the birth of intensive care

| Year | Where | What | Effect |
|---|---|---|---|
| 1928 | Boston (Harvard) | **Iron lung** (negative-pressure ventilator), Drinker & Shaw | Patients with respiratory paralysis could survive the acute phase |
| **1952** | **Copenhagen** | **Positive-pressure ventilation** (Bjørn Ibsen; manual bag via tracheostomy) during the city's polio epidemic | Bulbar/respiratory polio mortality fell from ~80–90% to ~40%; widely regarded as the **birth of the modern ICU** |
| 1950s | U.S. / Europe | Spread of mechanical ventilators and intensive-care units | Sustained lower case-fatality for severe polio |

*U.S. data signal:* CFR (deaths ÷ paralytic cases) fell from **~15% at the 1952
epidemic peak to ~7% by 1954–55** and stayed there.

## Measles — antibiotics for secondary infection

Most measles deaths came from **secondary bacterial pneumonia** and other
complications, not the virus directly — so antibacterial treatment mattered.

| Year | What | Effect |
|---|---|---|
| 1935–1937 | **Sulfonamide** antibiotics | First effective treatment of secondary bacterial infections |
| 1942–1945 | **Penicillin** enters clinical, then widespread civilian use (post-WWII) | Further reduced secondary-infection deaths |
| early 1900s→1950s | Improved nutrition, hydration, supportive care | Major contributor to the long pre-vaccine CFR decline |

*Signal:* the U.S. measles **death rate fell ~90% from 1900 to 1950 — before the
1963 vaccine** (see `early_mortality_rates.csv` and the early-mortality chart).

## Pertussis — supportive/critical care for infants

Pertussis deaths concentrate in **young infants** (respiratory failure, apnea,
secondary pneumonia), so infant critical care is decisive.

| Year | What | Effect |
|---|---|---|
| 1930s–1940s | Sulfa, then penicillin for secondary infection | Fewer secondary-pneumonia deaths |
| 1952 | **Erythromycin** (active against *B. pertussis*) | Reduces transmission/severity if given early |
| 1960s onward | **Neonatal/pediatric intensive care (NICUs)**, mechanical ventilation, oxygen | Lowered infant case-fatality independent of incidence |

## Cross-cutting

Oxygen therapy, intravenous fluids, improved nutrition, and the general rise of
hospital and critical care across the 20th century reduced deaths from many
infections **independent of any vaccine**. This is why death-based metrics, while
the most comparable for *severity* across eras, still **overstate the decline in
true infection rates**.

## Sources

- CDC MMWR, "Achievements in Public Health, 1900–1999: Control of Infectious
  Diseases" (MMWR 1999;48(29):621–629).
- History-of-medicine literature on the 1952 Copenhagen polio epidemic and the
  origins of intensive care (Ibsen; Berthelsen & Cronqvist reviews).
- Standard pediatric and infectious-disease references for antibiotic and
  critical-care timelines.
