<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 2 — Data Audit

> **What this phase does:** Challenge whether the data is trustworthy enough to carry the decision — six categories, findings with cited evidence, one disposition decision per finding before any algorithm runs.
> **Why it exists:** An unaudited dataset silently corrupts every downstream phase; a label-in-disguise in clustering means you paid to re-derive the 2020 rulebook.
> **You're here because:** You completed Phase 1 — Frame (`phase-01-frame.md`) and have a written frame to anchor findings to.
> **Key concepts you'll see:** six-category audit, contamination, sampling bias, missingness, label-in-disguise, baseline seasonality

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Playbook Phase 2 — Data Audit. My decision here is the
disposition per audit finding — cap, log-transform, exclude, flag, or
leave. I am not validating the data; I am deciding what to do with
what you find.

Copy the Phase 2 skeleton from journal/skeletons/phase_2_data_audit.md
into the project journal and fill the blanks as we go. Leave
dispositions as TODO — those are my calls.

Run the six-category audit against the source dataset(s). For every
finding in every category:

1. Duplicates — exact ID repeats. Report count + first 3 offending IDs.
2. Contamination — staff, bot, test, or integration accounts. Cite the
   column and rule that flags them. If no such column exists, say so.
3. Sparsity — records with fewer than the minimum useful observations
   (e.g. fewer than 3 transactions per customer). Report count and
   fraction.
4. Outliers — top-1% on dominant numeric features. Report the threshold
   and count.
5. Labels-in-disguise — any column that is itself a pre-existing
   segment assignment, tier, or rule output. Report column name and
   unique-value count.
6. Missingness — per-column NaN rate; flag any column >5% missing.

For every claim, cite the exact file and column (or function) you used.
If you cannot cite a file and a column, delete the claim.

Propose a disposition per finding — cap, log-transform, exclude, flag,
or leave — with a one-line reason each. I approve or overrule per
finding. Do NOT apply any disposition yet.

Do NOT use "blocker" unless you name the specific next phase I cannot
run. A 7% NaN rate is a finding, not a blocker.

When the audit table is complete with cited findings and proposed
dispositions, stop and wait for me to approve per finding.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
Dataset paths: src/retail/data/arcadia_customers.csv,
  arcadia_transactions.csv, arcadia_products.csv (5,000 customers,
  120,000 transactions, 400 SKUs).
Contamination rule: rows where email domain ends in @arcadia-internal.sg.
  If the column doesn't exist, say so — don't invent one.
Sparsity floor: customers with fewer than 3 transactions (cannot be
  clustered honestly — too little signal).
Outlier candidates: total_spend_sgd, visits_per_week (top-1% threshold).
Label-in-disguise suspect: any column named *_tier, *_segment, or
  *_score that predates this sprint.
Dollar business-impact framing: if you note the risk of skipping the
  audit, quote $45 per wrong-segment campaign and $3 per touch from
  PRODUCT_BRIEF.md §2 verbatim — do NOT invent a number.
Function source: if a column is engineered, cite the function in
  src/retail/backend/ml_context.py that produces it.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ All six audit categories addressed with counts, even if the count is zero
- ✓ Every finding cites a specific file and column (or function in `ml_context.py`)
- ✓ A proposed disposition (cap / log / exclude / flag / leave) with a one-line reason per finding
- ✓ Label-in-disguise check run on every column that looks categorical or "tier"-shaped
- ✓ Dispositions marked TODO — none applied yet
- ✓ A stop signal waiting for per-finding approval
- ✓ Viewer (http://localhost:3000) shows: data-quality summary panel populated with the audit table — six category rows, each with a finding count and pass / flagged / action-needed status

**Signals of drift — push back if you see:**

- ✗ "The data looks fine" / "no major issues" without per-category evidence ("please walk through all six categories; each needs a count even if it's zero")
- ✗ A finding without a column or function citation ("which file and which column produced this? please cite or delete")
- ✗ A disposition applied before approval ("please revert; dispositions are my call, not yours")
- ✗ A contamination rule without the column it runs on ("which column flags staff accounts? if no such column exists, say so")
- ✗ A dollar figure not quoted from `PRODUCT_BRIEF.md §2` ("please quote the §2 row")
- ✗ Viewer shows nothing new after CC reports the phase complete — CC may have described the work, not run it. Re-prompt: "show me the data-quality summary panel in the viewer"

---

## 3. Things you might not understand in this phase

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Six-category audit** — the specific six failure modes worth checking before any algorithm runs
- **Contamination** — records that don't represent the real population (staff, bots, test accounts) and will form their own spurious segments
- **Sampling bias** — the systematic ways the dataset may not represent the population you're trying to serve
- **Missingness** — missing values and why their pattern matters as much as their count
- **Label-in-disguise** — a pre-existing tier or segment column that would cause a model to re-derive the old rulebook rather than discover new structure
- **Baseline seasonality** — how predictable seasonal patterns (Black Friday) interact with outlier thresholds and affect what "typical" looks like

---

## 4. Quick reference (30 sec, generic)

### Six-category audit

The six things worth checking before ANY algorithm runs: duplicates (ID repeats), contamination (non-real users), sparsity (too few observations to learn from), outliers (extreme values that dominate distance calculations), labels-in-disguise (pre-existing rule outputs hiding as features), and missingness (NaN patterns). Each category gets a count and a proposed disposition. Skipping any of them means your model is building on a foundation you haven't checked.

> **Deeper treatment:** [appendix/02-data/data-audit.md](./appendix/02-data/data-audit.md)

### Contamination

Records that don't represent real users — staff accounts, bot traffic, integration-test accounts, partner API calls. In clustering, contaminated records don't just add noise: they form their own segment. If you ship a "4AM high-frequency buyer" segment that is actually your QA team, the CMO will notice before you do. Quantify contamination before you fit, not after.

> **Deeper treatment:** [appendix/02-data/data-audit.md](./appendix/02-data/data-audit.md)

### Sampling bias

The systematic ways the dataset underrepresents or overrepresents parts of the population. A dataset of "customers who transacted in the last 90 days" is biased toward active buyers — it silently excludes churned customers, seasonal buyers, and recently acquired customers. The bias isn't wrong, but it must be named: your model will only generalise to people who look like the population it was trained on.

> **Deeper treatment:** [appendix/02-data/data-audit.md](./appendix/02-data/data-audit.md)

### Missingness

Missing values (NaN) in a column are rarely random. A missing `last_login_date` often means the account was never activated; a missing `promo_response` often means the customer was never sent a promo. The PATTERN of missingness is as informative as the count. Blanket imputation hides the pattern. Your options are: impute (fill in an estimate), drop (remove the row/column), leave-as-NaN, or flag with a binary mask feature that preserves the missingness signal.

> **Deeper treatment:** [appendix/02-data/data-audit.md](./appendix/02-data/data-audit.md)

### Label-in-disguise

A column that is itself the output of a previous rule-based system — a loyalty tier, a risk band, a hand-authored segment flag. Including it as a feature means the ML model will rediscover the old rulebook rather than find new structure. In supervised learning this is a leakage bug. In clustering it's worse: the segmentation looks behavioural, is actually your 2020 rulebook in disguise, and the CMO correctly asks "why did I pay for this."

> **Deeper treatment:** [appendix/02-data/data-audit.md](./appendix/02-data/data-audit.md)

### Baseline seasonality

Retail data contains predictable seasonal patterns — Black Friday volume spikes, year-end slowdowns, school-holiday shifts. If your outlier thresholds are set on all-time data, they will either let Black Friday values through (because they're "normal for that week") or exclude them (because they're extreme vs annual mean). Decide which horizon your model serves before setting thresholds, or the thresholds will implicitly answer the question for you.

> **Deeper treatment:** [appendix/02-data/data-audit.md](./appendix/02-data/data-audit.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in Playbook
Phase 2 — Data Audit.

Read `workspaces/metis/week-05-retail/playbook/phase-02-data-audit.md`
for what this phase does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. label-in-disguise >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in Phase 2
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] All six audit categories addressed with a count (even if zero)
- [ ] Every finding cites a specific file and column or function
- [ ] Disposition proposed per finding (none applied yet)
- [ ] Label-in-disguise check run on every tier-shaped or categorical column
- [ ] No dollar figures invented — all quoted from `PRODUCT_BRIEF.md §2`

**Next file:** [`phase-03-features.md`](./phase-03-features.md)
