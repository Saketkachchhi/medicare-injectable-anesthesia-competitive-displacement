# Why the J2250 Cannibalization Play Failed — and How to Recover

**Competitive Displacement & Brand Erosion Analytics on Medicare CCLF Claims (2016–2018)**
*Injectable Anesthesia Market Basket: J1885 · J2250 · J2704 · J3010*

![Status](https://img.shields.io/badge/status-final-success)
![Domain](https://img.shields.io/badge/domain-Pharma%20Commercial%20Analytics-1a3a5c)
![Data](https://img.shields.io/badge/data-Medicare%20CCLF%20(2016--2018)-c0392b)
![Stack](https://img.shields.io/badge/stack-Python%20%7C%20pandas%20%7C%20matplotlib-2e86ab)
![Course](https://img.shields.io/badge/course-BIA--810%20Healthcare%20Analytics-555)
![License](https://img.shields.io/badge/license-MIT-green)

> **TL;DR.** A high-profile portfolio brand (J2250, midazolam) was launched to absorb the share of a declining market leader (J1885, ketorolac). The cannibalization play has failed: J2250 fell **−30%** in claims while a direct rival (J3010, fentanyl) grew **+165%** in the same window and **overtook the leader in revenue terms**. This repo contains the full reproducible analysis (Python notebook + slide deck) that names the real cause as a **retention crisis** (46.4% writer retention, zero High-Volume prescribers, 58% J2250↔J3010 patient overlap) and lays out a four-priority commercial playbook with sized prizes, 30/60/90-day execution plans, and per-territory KPIs.

---

## Table of Contents

1. [Project Overview & Business Problem](#project-overview--business-problem)
2. [Market Basket & Clinical Context](#market-basket--clinical-context)
3. [Data Infrastructure & Methodology](#data-infrastructure--methodology)
4. [Advanced Analytical Frameworks Applied](#advanced-analytical-frameworks-applied)
5. [Strategic Commercial Playbook](#strategic-commercial-playbook)
6. [Data Limitations & Nuances](#data-limitations--nuances)
7. [Repository Structure](#repository-structure)
8. [How to Reproduce](#how-to-reproduce)
9. [Team & Acknowledgements](#team--acknowledgements)

---

## Project Overview & Business Problem

The brief was a textbook portfolio-cannibalization case. A pharmaceutical manufacturer launched a *variant brand*, **J2250 (midazolam)**, with the explicit commercial intent of absorbing the share that its mature **market leader J1885 (ketorolac)** was bleeding to competitors. Three years of Medicare CCLF claims (2016–2018) were made available to test whether the strategy was working.

It is not. The data refutes the cannibalization thesis on every measurable dimension.

Between 2016 and 2018, J1885 claims share fell from **73.8% → 58.9%**. Almost none of that vacated share migrated to our own brand. The competitor, **J3010 (fentanyl)**, grew from **14.3% → 28.8%** and tripled its absolute claim volume from **609 → 1,613** (a **+165%** two-year lift, **+62.7% CAGR**). J2250 — the brand that was supposed to catch the falling share — slipped from **10.0% → 5.4%** in claims and **−30%** in absolute volume (−16.1% CAGR). On the dollar side it is even starker: J3010 revenue share grew from **30.1% → 44.4%** and has **already passed J1885 in Medicare-paid dollars** even though J1885 still nominally leads in claim count.

A patient-flow audit confirms the displacement is direct and one-for-one. Of the **2,017 patients on J1885 in 2016**, only ~6% had appeared on J2250 by 2018, but **~34% had migrated to J3010**. And **58% of all J2250 patients (570 of 982) have also been treated with J3010** — meaning the competitor is no longer just winning *new* patients; it is treating *our* patients alongside us.

This repository packages the full analysis behind those findings, the strategic reframe they triggered, and the sized commercial actions that follow.

---

## Market Basket & Clinical Context

Before any number was modeled, the four-HCPCS market basket was re-examined pharmacologically. The conclusion — emphasized as the "pharmacological reframe" throughout the analysis and the panel deck — is that **the cannibalization assumption was never clinically plausible** because J2250 and J1885 are not in the same drug class.

| HCPCS | Generic | Drug Class | Clinical Role | Role in this study |
| --- | --- | --- | --- | --- |
| **J1885** | Ketorolac tromethamine | NSAID | Short-term moderate-to-severe pain; pre/post-op analgesic | Market Leader — the declining brand the play was meant to defend |
| **J2250** | Midazolam HCl | Benzodiazepine | Induction of general anesthesia / sedation | Variant Brand — the focus of the recovery strategy |
| **J2704** | Propofol | IV anesthetic / sedative | Sedation / induction | Alternate Competitor — J2250's *true* clinical substitute |
| **J3010** | Fentanyl citrate | Synthetic opioid | Analgesia during anesthesia, induction, recovery | Main Rival — the brand capturing the share J2250 was supposed to absorb |

Strategically this is the single most important insight in the project. The original portfolio play assumed J1885 → J2250 substitution; the pharmacology says J2250's real competitive set is **J2704 (propofol) and J3010 (fentanyl)** in the induction / sedation conversation. Every detail aid, KOL program, and piece of clinical evidence has to be reset against that competitive frame, not against J1885. The deck makes this the opening "Structural Truth" of the recommendation section.

---

## Data Infrastructure & Methodology

The raw source was the Medicare **Common Claims Linked File (CCLF)** delivered in five compressed parts, supplemented with HCP demographics, patient demographics, ZIP-to-territory mapping, ICD-10 → diagnosis-specialty mapping, and a HCPCS procedure-code map. The analytical pipeline is a single, fully-runnable Python notebook (22 code cells, 48 markdown cells) built in pandas + matplotlib; outputs are deterministic and verified by inline assertions.

The pipeline normalizes inputs, filters to the four-HCPCS market basket, and produces an analysis-ready frame of **15,262 brand line items across 15,139 unique claim IDs** out of **28,368 total dataset rows** (17 records from 2015 are dropped as out-of-window). Each modeling decision is explicitly captured and justified:

| Decision | Choice / Value | Rationale |
| --- | --- | --- |
| Time window | 2016–2018 | Per project brief. 17 line items from 2015 dropped as out-of-window. |
| Brand attribution | Line-level `clm_line_hcpcs_cd ∈ {J1885, J2250, J2704, J3010}` | Each line identifies a specific drug administration; aggregating to claim-ID would double-count administrations of multiple basket products on the same encounter. |
| Date parsing | `clm_from_dt` via `pd.to_datetime`; `clm_thru_dt` normalized from mixed ISO/US formats | Resolves date-format inconsistencies surfaced at runtime. |
| ZIP code handling | Cast to 5-digit zero-padded string before territory join | Preserves leading zeros (e.g., `01104`). |
| Diagnosis specialty | First alphabet of `clm_dgns_cd` mapped via Diagnosis Code Mapping | Per assignment guidance; line-level rather than principal-diagnosis. |
| HCP definition | Unique `fac_prvdr_npi_num` (10-digit NPI) | Standard claims convention. |
| New writer | NPI's first observed claim year for the brand | Subject to a 2016 boundary effect (data start year) — flagged everywhere it appears. |
| Continuing writer | NPI active in both years of the period | Per assignment. |
| Revenue / spend | `clm_line_cvrd_pd_amt` (Medicare-paid amount) | Cleanest available proxy for brand revenue; Medicare-only, not commercial book. |

**Data-quality checks verified at runtime.** Row count assertion (`28,368` total), out-of-window record exclusion (17 rows in 2015), share columns sum to 100% per year within float tolerance, and date-format inconsistencies resolved during preparation. Upstream typos in territory labels (`Philedelphia`, `Pittsburg`) are intentionally preserved as-is so figures match the source data exactly.

The final dataset spans **22 territories across 4 regions**, with **3,396 J1885 patients · 982 J2250 · 636 J2704 · 2,079 J3010**.

---

## Advanced Analytical Frameworks Applied

The required market-share and market-driver analyses (Q1 and Q2 in the brief) are present, but the analytical depth of the project lives in three additional frameworks that test the cannibalization claim directly and turn the findings into named, sized commercial actions.

### Cohort Switcher Transition Matrices (longitudinal patient-level brand switching)

For every patient observed on a basket brand in 2016, the matrix tracks which basket brands they were observed on by 2018. This is the textbook cannibalization-failure metric: of the **2,017 J1885 patients in 2016, only ~6% had moved to J2250** by 2018, while **~34% had moved to J3010**. A second view — a one-to-one J2250↔J3010 overlap — shows **570 of J2250's 982 patients (58%) have also received J3010**, leaving only 412 J2250-exclusive patients. The intended portfolio handover is not happening; the competitor is the *destination brand* for J1885 patients, and J2250 patients are increasingly being co-treated with the rival rather than retained. The deck uses this chart as the proof-point that the portfolio strategy must be replaced, not refined.

### HCP Behavioral Segmentation (Disease-Aware → Trialist → Rising Star → High-Volume)

Each NPI that wrote a basket brand in 2018 is bucketed by annual claim volume into a four-tier behavioral segment:

- **Disease-Aware** — 1 claim/year
- **Trialist** — 2–4 claims/year
- **Rising Star** — 5–9 claims/year
- **High-Volume** — 10+ claims/year

The result is the single most decisive chart in the project. **J2250 has zero High-Volume writers and only 43 Rising Stars — 90% of its base sits at 1–4 claims/year.** J3010, by contrast, has **96 High-Volume writers (19.4%) and 262 Rising Stars (52.9%)**, with only 3.6% of its base in the Disease-Aware tier. The asymmetry explains *why* J3010 wins independent of any acquisition activity: its writers are deeply embedded in the brand, while J2250 writers try it once and stop. Stacked alongside a **writer-retention rate** view (J1885 ≥99% · J3010 94.5% · J2250 **46.4%** · J2704 55.1%), the segmentation reframes the problem from "we need more writers" to **"we need to deepen and retain the ones we already have."**

### Territory-Level Competitive Displacement Matrix

For each of the **22 territories**, J2250 YoY claim change (2017 → 2018) is plotted against J3010 YoY change on the same axis to produce a side-by-side "mirror" of losses and gains. The matrix shows that **15 of 22 territories declined for J2250**, but only four are in *critical decline* (worse than −50%): **St. Louis (−72.7%), Phoenix (−70.0%), LA-San Diego (−57.9%), New York (−57.5%)**. In every one of those four — and in Minneapolis (−53.3%) — J3010 grew. New York alone moved from 33 to 153 J3010 claims (+364%) while J2250 fell from 40 to 17. Aggregated across the top-5 declining territories, **J2250 lost 76 claims** while **J3010 gained 121** in the same markets — direct, asymmetric capture, not market shrinkage. The matrix also surfaces the *positive* tail: **6 territories grew for J2250** (Pittsburg +30%, Detroit +20%, Charlotte +20%, Houston +14.3%, Chicago +11.1%, San Jose +9.5%) and are treated as commercial-excellence benchmarks whose playbook should be reverse-engineered and replicated in the four emergency markets.

A complementary **quarterly trend view** dates the inflection point precisely: **J3010 momentum accelerates between Q3 2017 and Q1 2018** — the most pronounced acceleration of any brand in the window. That six-month range is flagged to field intelligence as the highest-probability window for a competitor event (formulary win, sales-force expansion, KOL launch, or sample ramp).

---

## Strategic Commercial Playbook

The Q3 recommendations are deliberately **sequenced, sized, and discipline-bounded**. Four priorities, each with an action, a target, a sized prize, and a tracked KPI; the deck packages them into a single execution-plan slide with explicit 30/60/90-day milestones and a "what we will NOT pursue" list to protect commercial focus.

**Priority 1 — Fix Writer Retention Before Spending on Acquisition.** The 46.4% J2250 retention rate means more than half the writer base churns every year; no acquisition program can outrun that. Build the NPI list of **~148 J2250 writers active in 2017 but absent in 2018**, route each personally to the most senior territory rep, and run a structured re-engagement protocol (clinical case review, peer-to-peer programs, samples, patient-support co-promotion).
**Sized prize:** lift retention from 46.4% → 65% in 12 months ≈ recover 50–90 writers ≈ **+120 to +200 incremental claims/year** at a baseline of 2.5 claims/writer.
**30/60/90:** extract NPI list and brief reps → first-touch outreach to 100% of list → measure re-engagement conversion and refine the playbook.
**KPI:** monthly writer retention rate vs prior cohort.

**Priority 2 — Convert Trialists into Rising Stars.** With zero High-Volume writers and 90% of J2250's base at 1–4 claims/year, the highest-leverage move is depth, not breadth. Target the **284 Trialists** with quarterly clinical case studies, dosing-flexibility detail aids for the dominant 61+ patient segment, and peer-speaker events anchored on our highest-volume J2250 writer.
**Sized prize:** convert 20% of Trialists (~57 HCPs) from 3 → 6 claims/year ≈ **+170 incremental claims/year at zero acquisition cost**. At the observed 2018 avg paid/line of **$41.68**, that is **~$7K direct Medicare revenue uplift** before any commercial-book multiplier.
**30/60/90:** define Trialist target list per territory → deploy detail aids and case studies → measure claims-per-HCP shift.
**KPI:** % of Trialists migrating to Rising Star tier per quarter.

**Priority 3 — Declare Four Emergency Territories.** **St. Louis, Phoenix, LA-San Diego, and New York** each lost more than half their J2250 volume in a single year; in those same four markets J3010 added 165+ claims. Audit rep activity logs and formulary status in each within 30 days. In NY and LA, increase rep call frequency and run NPP campaigns; in St. Louis and Phoenix, deploy small-market-focused programs.
**Sized prize:** recover 50% of 2018 lost volume in these four markets ≈ **+30 short-term claims plus writer-base protection** that compounds across years.
**30/60/90:** root-cause audit (rep, formulary, KOL) → corrective interventions launched → review trajectory and escalate to the next 5 declining territories if needed.
**KPI:** monthly claims volume per territory vs Q4 2018 baseline.

**Priority 4 — Defend the Anesthesiology Base.** Anesthesiology is the must-win specialty — **228 unique writers, 2.5× the next specialty**. Ring-fence the top 30 anesthesiology writers in the J2250 base with KOL programs, advisory boards, and real-world evidence partnerships.
**Sized prize:** hold this segment at 2017 share ≈ **avoid losing the next ~150 claims/year** that would otherwise leak to J3010.
**KPI:** claim share within Anesthesiology specialty by quarter.

**Discipline list — what we will *not* pursue.** Net-new HCP recruitment until retention is above 65% (acquiring writers we cannot retain is wasted spend). National brand campaigns (the dynamics are geographic and HCP-specific; broadcast spend dilutes ROI). Repositioning against J1885 (the pharmacological reframe makes that competitive frame obsolete — we compete with J2704 and J3010).

**Aggregate sized prize.** Across Priorities 1 + 2 alone, the modeled incremental volume is **+290 to +370 J2250 claims/year**, recoverable inside a single fiscal year with zero net-new HCP acquisition spend.

---

## Data Limitations & Nuances

The analysis is honest about what Medicare CCLF claims data can and cannot tell us, and every recommendation is sized within those bounds.

**Medicare-only data boundary.** Conclusions are derived from Medicare CCLF claims and cannot be safely generalized to commercial or Medicaid books without IQVIA NPA / Xponent overlays. The shift to revenue share (J3010 surpassing J1885 in Medicare-paid dollars) could be over- or understated in the all-payer view.

**Tail-territory sample sizes (<30 claims/year).** Several of the "biggest decline" territories carry small denominators, which means very large percentage swings can be partly noise. Recommendations are kept directional and lean on **absolute claim counts** wherever possible (e.g., "+121 J3010 claims gained" rather than "+364% growth in NY") to avoid over-reading thin tails.

**2016 boundary effect for new writers.** Because the data window starts in 2016, every NPI's *first observed* year is 2016 by construction. The Chart 12 "new writer" series therefore equals total writers for that year. The true acquisition trend lives in **2017 and 2018 only**; the notebook and deck both flag this explicitly so the 285 → 111 → 34 J2250 pipeline-collapse number is read correctly.

**Patient-switcher matrices are inferred, not observed.** Without ground-truth Rx-level data (Xponent / NPA), the cohort-switcher and J2250 ↔ J3010 overlap analyses identify *co-treatment patterns* in Medicare claims, not switching events at the prescription level. The directional signal is unambiguous, but the *named NPI list* of switchers requires NRx/TRx data we do not have in scope.

**Diagnosis specialty is line-level, not principal.** The first-character mapping of `clm_dgns_cd` to specialty was validated as supplementary and did not change any conclusion, but line-level diagnoses are an approximation of the principal-diagnosis attribution a payer system would use.

**Critical data gaps explicitly named.** The analysis is missing **NRx vs TRx** (cannot separate acquisition vs refill failure), **payer mix and formulary tier** (a single regional formulary win can explain an entire territory's collapse and is currently invisible), **CRM / Veeva call activity** (no calls-to-claims conversion is possible — coverage vs. message-recall failure cannot be separated), **speaker-program and sample data** (cannot replicate J3010's likely 2016 medical-education push that added 344 new writers), **adherence / persistency**, and **primary VOC research** explaining *why* HCPs are choosing J3010. The notebook's Q4 section catalogues each missing dataset and pairs it with the specific decision it would change — i.e., the gaps are documented as a prioritized intelligence backlog, not as a caveat.

**Upstream label preservation.** Typos in territory data (e.g., `Philedelphia`, `Pittsburg`) are intentionally preserved as-is so all numerical results match the source data exactly; no impact on the conclusions.

---

## Repository Structure

```
medicare-injectable-anesthesia-competitive-displacement/
├── README.md                                          ← this file
├── LICENSE                                            ← MIT
├── .gitignore
├── notebooks/
│   └── Healthcare_Analytics_End_Term_FINAL.ipynb      ← 70 cells (22 code · 48 markdown)
├── reports/
│   ├── Healthcare_Analytics_End_Term_FINAL.html       ← rendered nbconvert export
│   └── Healthcare_Analytics_End_Term_REPORT.pdf       ← full written project report
├── presentation/
│   └── BIA810_Final_Presentation.pptx                 ← 36-slide panel deck
└── scripts/
    └── html_to_ipynb.py                               ← reverse-engineer .html → .ipynb
```

---

## How to Reproduce

The notebook is self-contained. Clone the repo, install the lightweight dependencies, and run end-to-end.

```bash
git clone https://github.com/Saketkachchhi/medicare-injectable-anesthesia-competitive-displacement.git
cd medicare-injectable-anesthesia-competitive-displacement
python -m venv .venv && source .venv/bin/activate
pip install pandas numpy matplotlib jupyterlab beautifulsoup4
jupyter lab notebooks/Healthcare_Analytics_End_Term_FINAL.ipynb
```

**Rebuild the notebook from the HTML export.** The `scripts/html_to_ipynb.py` utility converts the rendered nbconvert HTML back into a clean executable `.ipynb` — useful for auditors who only received the read-only HTML deliverable:

```bash
python scripts/html_to_ipynb.py \
    reports/Healthcare_Analytics_End_Term_FINAL.html \
    notebooks/Healthcare_Analytics_End_Term_FINAL.ipynb
```

The script preserves headings, GitHub-flavored tables, lists, fenced code, inline formatting, and image references. Output is a valid `nbformat 4.5` document with no external dependencies beyond `beautifulsoup4` and the Python standard library.

> *Data note:* the underlying Medicare CCLF files are not redistributed in this repository. Recipients of the dataset under the course license should place the raw `.csv.gz` parts under `data/raw/` and the mapping files under `data/mappings/`; paths are configurable in the first code cell of the notebook.

---

## Team & Acknowledgements

**J-FIVE — Team Healthcare Commercial Analytics (Spring 2026)**

- **Saket Kachchhi** — Project Lead
- **Aneesh Vishnu** — Strategy Lead
- **Nikhil Sonawane** — Execution Lead
- **William Reccoppa** — Lead Analyst, Market Drivers
- **Aditya Patel** — Market Research Lead

**Course:** BIA-810 Healthcare Data & Analytics · **Faculty:** Prof. Sanjiv Koshal

---

*This repository is an academic case study. Brand names, indications, and dollar figures are sourced exclusively from the supplied Medicare CCLF dataset and reflect Medicare-paid volume only; they should not be interpreted as representations of any real manufacturer's commercial position. Recommendations are directional, sized within the data-limitation envelope above, and are intended as a portfolio demonstration of pharmaceutical commercial-analytics methodology.*
