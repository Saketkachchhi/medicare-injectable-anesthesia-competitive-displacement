# LinkedIn Announcement (drop-in)

Use either the short version (recommended for the feed) or the long one (for an in-feed article / "Featured" section). Replace `<GITHUB_URL>` with your actual repo URL after `git push`.

---

## Short version (~1,300 characters — sits cleanly in the feed)

Just open-sourced my BIA-810 Healthcare Analytics final project: a competitive-displacement and brand-erosion study on a Medicare CCLF claims dataset (2016–2018) for an injectable-anesthesia market basket.

The brief was a classic portfolio-cannibalization case. The variant brand (J2250, midazolam) was launched to absorb the share of a declining leader (J1885, ketorolac). The data tells a very different story:

→ J2250 fell **−30%** in claims; the rival (J3010, fentanyl) grew **+165%** and has already **overtaken the leader in Medicare-paid revenue**.
→ Writer retention for J2250 is **46.4%** — the brand rebuilds its base from scratch every year.
→ **58%** of J2250 patients have also been treated with J3010. Direct, one-for-one competitive capture.
→ The cannibalization assumption was pharmacologically flawed from day one: a benzodiazepine sedative was never clinically substitutable for an NSAID analgesic.

The repo includes the full Python notebook (cohort switcher matrices, HCP behavioral segmentation, territory-level displacement matrix, quarterly inflection analysis), the panel deck, and a small utility script (`html_to_ipynb.py`) that reverse-engineers an nbconvert HTML export back into a clean `.ipynb`.

Modeled sized prize: **+290 to +370 incremental J2250 claims/year**, recoverable inside a single fiscal year with zero net-new HCP acquisition spend.

Repo: <GITHUB_URL>

#PharmaAnalytics #HealthcareData #CommercialAnalytics #Python #DataScience #BIA810

---

## Long version (for the "Featured" section or a LinkedIn article)

**Why a portfolio cannibalization play failed — and what 3 years of Medicare claims revealed about it.**

For my BIA-810 Healthcare Analytics final at Stevens, my team and I were handed the type of brief every pharmaceutical commercial-analytics group runs into eventually: a manufacturer launched a variant brand (J2250, midazolam) to absorb the share of its declining leader (J1885, ketorolac). Three years of Medicare CCLF claims later, did the strategy work?

It didn't — and the data shows why in a way that's almost uncomfortable to read.

Between 2016 and 2018, J1885 claim share fell from 73.8% to 58.9%. Almost none of that vacated share landed on J2250. The real beneficiary was the rival, J3010 (fentanyl), which grew from 14.3% to 28.8% in claims (+165% in absolute volume, +62.7% CAGR) and has already passed the leader in Medicare-paid revenue. J2250 lost 30% of its claim volume in the same window.

Three findings ended the debate:

1. **The cannibalization premise was never clinically valid.** Midazolam is a benzodiazepine sedative; ketorolac is an NSAID analgesic. They sit at different points in the perioperative pathway. J2250's *real* competitive set is propofol (J2704) and fentanyl (J3010), not ketorolac.

2. **It's a retention crisis, not an acquisition crisis.** J2250's writer retention is 46.4% — more than half the writer base churns every year. The HCP behavioral segmentation makes it brutally clear: J2250 has *zero* High-Volume writers and only 43 Rising Stars; 90% of its base sits at 1–4 claims/year. J3010 has 96 High-Volume writers and a 94.5% retention rate. The brands are not playing the same game.

3. **The displacement is direct.** 58% of J2250 patients have also received J3010, and only ~6% of the leader's 2016 patient cohort migrated to J2250 by 2018 (vs. ~34% to J3010). The competitor isn't winning a vacuum — it's treating our patients.

The recovery playbook follows naturally: fix retention before spending on acquisition (lift 46% → 65% over 12 months = +120 to +200 incremental claims), convert 20% of the 284 Trialists into Rising Stars (+170 claims/year at zero acquisition cost), declare four emergency territories (St. Louis, Phoenix, LA-San Diego, New York — together they lost 70+ J2250 claims while J3010 gained 165+), and ring-fence the 30 most important anesthesiology KOLs.

The repo includes the full Python notebook, the panel deck, and a small `html_to_ipynb.py` utility that reverse-engineers an nbconvert HTML export back into a clean executable `.ipynb` — built for the auditor who only got the read-only HTML.

Special thanks to my J-FIVE teammates — Aditya Patel, Aneesh Vishnu, Nikhil Sonawane, William Reccoppa — and to Prof. Sanjiv Koshal for the brief.

Repo: <GITHUB_URL>

#PharmaCommercialAnalytics #HealthcareAnalytics #DataScience #Python #BrandStrategy #Medicare #HCPSegmentation #BIA810
