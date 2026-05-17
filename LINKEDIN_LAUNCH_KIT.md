# LinkedIn Launch Kit
*Recruiter- and exec-targeted post + 6-slide PDF carousel storyboard*

This file contains the two pieces of launch copy that pair with the GitHub repo:

- **Phase 3** — a high-conversion LinkedIn feed post, optimized for data-science recruiters and pharmaceutical / healthcare executive visibility.
- **Phase 4** — a slide-by-slide storyboard for the 6-page PDF carousel you'll attach to that post.

Repo: https://github.com/Saketkachchhi/medicare-injectable-anesthesia-competitive-displacement

---

# Phase 3 — LinkedIn Post (drop-in copy)

> Open with the post body. Carousel attached below. Do **not** put the hashtags in the first three lines — LinkedIn's algorithm down-ranks posts that open with tags. Hashtags go at the very bottom.

---


**Top-line market-share charts are where most pharma post-mortems stop.**
**They're also where the actual story gets buried.**

A variant brand in my latest analysis looked like a routine portfolio underperformer: −30% in claims, sliding share, classic "spend more on detailing" diagnosis.

Three years of Medicare CCLF claims (2016–2018, ~28K rows, 22 territories, 4-HCPCS market basket) said something completely different. The brand wasn't losing the market. **It was being displaced — patient by patient, writer by writer — by one specific competitor.** And the cannibalization strategy that was supposed to save it had been pharmacologically impossible from day one.

To prove it, I built two analytical layers that almost never show up in the top-line deck:

**🔁 Cohort Switcher Transition Matrices**
For every patient on the declining market leader in 2016, I tracked which basket brand they were treated with by 2018. Only ~6% had moved to *our* variant. ~34% had moved to the rival. The "portfolio handover" wasn't happening — the destination brand was the competitor.

**👥 HCP Behavioral Segmentation (Disease-Aware → Trialist → Rising Star → High-Volume)**
Bucketing every writer by annual claim volume exposed the real failure mode:
→ Our brand: **0 High-Volume writers, 90% Trialists or below, 46.4% retention**
→ The rival: **96 High-Volume writers, 53% Rising Stars, 94.5% retention**
The brands weren't playing the same game. One was being adopted; the other was being sampled and abandoned.

When you stack the matrix + the segmentation, the displacement gets a name and a price tag:

📉 **58%** of our variant's patients are already being co-treated with the rival
📉 Four "emergency" territories lost **70+** claims in a single year while the rival gained **165+** in the same markets
📈 Fixing retention (46% → 65%) + converting 20% of Trialists into Rising Stars = **+290 to +370 incremental claims/year at zero net-new HCP acquisition spend**

The discipline-list ended up being more valuable than the recommendations:

❌ **No** net-new HCP recruitment until retention is above 65% — acquiring writers you can't retain is wasted spend
❌ **No** national broadcast campaigns — the dynamics are geographic and HCP-specific
❌ **No** repositioning against the legacy leader — the pharmacology said it was never a real comparator

Top-line metrics tell you *that* a brand is losing. Switcher matrices and behavioral segmentation tell you *who is taking it, where, and at what tier of clinical depth* — which is the only level at which a commercial team can actually intervene.

Full Python notebook (pandas + matplotlib), 36-slide panel deck, and a small utility script that reverse-engineers an nbconvert HTML export back into a clean executable .ipynb — all open-sourced:

🔗 https://github.com/Saketkachchhi/medicare-injectable-anesthesia-competitive-displacement

Huge thanks to my J-FIVE teammates — Aditya Patel, Aneesh Vishnu, Nikhil Sonawane, William Reccoppa — and Prof. Sanjiv Koshal for the brief.

If you work on pharma commercial analytics, HCP targeting, or competitive intelligence and want to swap notes, my inbox is open.

#PharmaCommercialAnalytics #HealthcareAnalytics #DataScience #CompetitiveIntelligence #BrandStrategy #Pharma #MedicareData #HCPSegmentation #Pandas #Python #PortfolioProject #LifeSciences #MarketAccess

---

### Posting tips

- **Best time to post:** Tue–Thu, 8:00–10:00 am or 5:00–6:00 pm in the recruiter's timezone.
- **Attach the carousel PDF below** — LinkedIn boosts dwell time on multi-page documents and dwell time is the single biggest reach signal on the platform.
- **Reply to the first 3 comments within 30 minutes.** That's the algorithm's "is this conversation alive?" window.
- **Tag thoughtfully:** tag your professor and team members in a comment, not in the post body (tag-in-body suppresses reach when the tagged accounts don't immediately engage).

---
---

# Phase 4 — PDF Carousel Storyboard (6 slides)

Build this as a 1080 × 1350 px PDF carousel (LinkedIn's preferred 4:5 aspect ratio — biggest mobile feed real-estate). Use a clean 2-color palette pulled from the notebook's actual chart styling: **deep navy `#1a3a5c`** (our variant), **brick red `#c0392b`** (the rival), warm gray `#555` for body, soft cream `#f7f3ec` for background. One typeface, two weights (Inter Bold for headlines, Inter Regular for body). Reserve the bottom-right corner of every slide for a small "swipe →" cue and your handle.

---

## Slide 1 — The Hook

**Header / Title text**
> Top-line market-share charts told us the brand was losing.
> The patient-flow matrix told us *who was taking it*.

**Subtitle**
A 3-year competitive-displacement case study on a Medicare CCLF injectable-anesthesia market basket.

**Core visual concept / layout**
- Full-bleed background image: stylized line chart with two diverging curves — one navy curve falling (`−30%`), one red curve rising (`+165%`) — crossing at roughly the 60% mark of the page.
- Large headline overlay in white on a navy-to-transparent gradient at the bottom third.
- Top-left corner: small "Case Study · 2016–2018 · Medicare CCLF" pill.
- Top-right corner: small Stevens / J-FIVE attribution chip.

**Key takeaway bullets (do not list visibly — use as designer brief)**
- The hook is the gap between the *top-line* story and the *patient-flow* story.
- This slide's only job is to stop the thumb-scroll. Zero numbers in the headline itself; the chart does the lifting.

---

## Slide 2 — The Trap

**Header / Title text**
> The −30% headline hid the real problem.

**Core visual concept / layout**
- Three-row stacked layout. Each row is a "what the top-line said vs. what the data showed" pair.
- Left column: muted gray icon + the assumed narrative.
- Right column: navy/red icon + the actual finding, larger type.
- Faint horizontal hairlines between rows.

**Key bullet points**
- **Top-line said:** "Variant brand losing share — spend more on detailing."
**Data said:** Brand isn't *losing* the market. It's being *replaced*, one writer at a time.
- **Top-line said:** "Cannibalization plan needs a relaunch push."
**Data said:** Cannibalization was never pharmacologically possible — a benzodiazepine sedative is not substitutable for an NSAID analgesic. Wrong competitive frame from day one.
- **Top-line said:** "We need to acquire more new writers."
**Data said:** 90% of existing writers churn or sample-and-stop. Acquisition without retention is a leaky bucket.

---

## Slide 3 — The Method (the actual analytical edge)

**Header / Title text**
> Two analytical layers most post-mortems skip.

**Core visual concept / layout**
- Split the slide into two equal vertical panels.
- Left panel ("Cohort Switcher Matrix"): a 4×4 mini-grid with rows = 2016 brand cohort, columns = 2018 destination. Highlight the diagonal in light gray and bolt-red the off-diagonal cell where the rival captured ~34% of the leader's 2016 patients.
- Right panel ("HCP Behavioral Segmentation"): a 4-tier vertical funnel with tier labels (Disease-Aware → Trialist → Rising Star → High-Volume) and two side-by-side stacked bars showing our brand (top-heavy in the lower tiers) vs. the rival (top-heavy in the upper tiers).
- Bottom strip: one-line caption — "Built in pandas. Reproducible. Fully open-source."

**Key bullet points**
- **Cohort Switcher Transition Matrix** — for every patient on a basket brand in 2016, track where they ended up in 2018. Replaces vague "market shift" language with a directional flow you can chase down with field intel.
- **HCP Behavioral Segmentation** — bucket each NPI by annual claim volume into four behavioral tiers. Reframes the problem from "we need more writers" to "we need deeper writers."
- Stacked together, these two views turn a generic erosion narrative into a **named, sized, geo-specific commercial intervention.**

---

## Slide 4 — The Three Findings That Ended the Debate

**Header / Title text**
> Three numbers reframed the entire strategy.

**Core visual concept / layout**
- Three giant stat blocks, vertically stacked, each block split into a left "stat" panel (huge number, brand color) and a right "what it means" panel (one sentence).
- Background: subtle horizontal hairlines, no other decoration.
- Use the navy + brick-red palette to color-code: navy for our brand stats, brick-red for the rival's.

**Key bullet points (one per block)**
- **46.4%** — *Our brand's writer retention.* We rebuild the writer base from scratch every year. No acquisition spend survives this churn.
- **0** — *Our brand's High-Volume prescribers (10+ claims/year).* The competitor has 96. The brands are not playing the same game.
- **58%** — *Of our brand's patients have also received the rival.* Direct, one-for-one competitive co-treatment. Not a vacuum-fill story.

---

## Slide 5 — The Sized Prize Playbook

**Header / Title text**
> Four priorities. Sequenced. Sized. Sales-rep-ready.

**Core visual concept / layout**
- 2×2 quadrant grid. Each quadrant is one priority. Number badge in the corner (01–04). Bold action verb headline. Sized prize in a colored ribbon at the bottom of the quadrant.
- Border each quadrant in navy. Ribbon in brick-red with white type for maximum scan-ability.
- Bottom strip: a small "30/60/90" three-dot timeline icon with a single line of caption text.

**Key bullet points (one per quadrant)**
- **01 · FIX WRITER RETENTION**
Re-engage ~148 lapsed writers. Personal senior-rep outreach. **Sized prize: +120–200 claims/year.**
- **02 · CONVERT TRIALISTS → RISING STARS**
Target the 284 Trialists with clinical case studies + peer-speaker events. Double volume for 20% of them. **Sized prize: +170 claims/year at zero acquisition cost.**
- **03 · DECLARE 4 EMERGENCY TERRITORIES**
St. Louis, Phoenix, LA–San Diego, New York. 30-day rep & formulary audit. **Sized prize: +30 short-term claims + writer-base protection.**
- **04 · RING-FENCE THE ANESTHESIOLOGY KOL BASE**
Named-NPI lock on the top 30 anesthesiology writers. KOL programs, RWE partnerships. **Sized prize: avoid leaking ~150 claims/year.**
- Footer line: *Aggregate sized prize: **+290 to +370 incremental claims/year**, recoverable inside a single fiscal year, zero net-new HCP acquisition spend.*

---

## Slide 6 — The Discipline List + CTA

**Header / Title text**
> What we will NOT pursue (and why that matters more than what we will).

**Core visual concept / layout**
- Top two-thirds: three "❌" rows on a near-white background, each with a short headline + one-sentence rationale in muted gray.
- Bottom third: a dark-navy CTA panel with a clean QR code on the left, three lines of CTA copy on the right, and your handle in the footer.

**Key bullet points**
- ❌ **No net-new HCP recruitment until retention is above 65%.** Acquiring writers you cannot retain is wasted spend.
- ❌ **No national broadcast campaigns.** The dynamics are geographic and HCP-specific; broadcast spend dilutes ROI.
- ❌ **No repositioning against the legacy leader.** Pharmacologically obsolete competitive frame.
- CTA copy:
**The full notebook, the deck, and the open-source `html_to_ipynb` utility:**
🔗 https://github.com/Saketkachchhi/medicare-injectable-anesthesia-competitive-displacement
*Open to data-science roles in pharma commercial analytics, competitive intelligence, and HCP targeting. Let's talk.*
- Footer: your name · MS Business Intelligence & Analytics (Stevens) · saketkachchhi@gmail.com

---

## Production checklist

- [ ] Export at 1080 × 1350 px per page, save as a single multi-page PDF.
- [ ] Embed fonts. Test on mobile (LinkedIn previews crop heavily on Android).
- [ ] Add 24px safe margins inside every page; LinkedIn occasionally crops 12–16 px on the right.
- [ ] First page must be readable with the audio off, the carousel collapsed to a thumbnail, and the user scrolling at speed — that's the bar.
- [ ] Re-export the QR code on slide 6 *after* the GitHub repo is live; the link inside the QR is the highest-friction conversion in the whole funnel.

That's the launch kit. The post does the cold-stop; the carousel does the proof; the repo closes the loop.
