<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Phase 2 — Data Audit

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 2 of 8 — Data Audit
 LEVERS:        outlier handling · missingness · contamination filters · sampling
──────────────────────────────────────────────────────────────────
```

### Concept

Before you point any algorithm at the data, challenge whether the data is trustworthy enough to carry the decision. Six categories: duplicates, contaminated populations, sparsity that makes rows unusable, outliers that will dominate the result, fields that are labels in disguise, missingness with unknown behaviour.

### Why it matters (SML lens)

- Reinforces Week 2's leakage lesson — a diagnosis code recorded at discharge is a perfect predictor of readmission because it encodes the answer.
- Reinforces Week 3's outlier finding — a single merchant's 0.1% of transactions drove 14% of the fraud score.
- Reinforces Week 4's missingness rule — you don't know what your model does with a NaN until you look.
- Dollar framing: skipping the audit in Week 3 would have cost $22,000/month in false alarms. Same logic here: accepting the top-1% spenders silently means every customer segment becomes "rich vs not rich."

### Why it matters (USML lens)

- Outliers dominate distance-based clustering more than they bias a supervised model — one customer who spends 30× the median can form their own cluster and shift every other boundary. Decide NOW: cap, log-transform, or exclude.
- A **label-in-disguise** in SML is a leakage bug. In USML it's worse: a pre-existing tier column or a 2020 hand-authored segment flag will cause the clustering to rediscover that old rule, and the CMO will correctly ask "why did I pay for this."
- Singleton customers (one transaction ever) cannot be clustered honestly — inventing behaviour from noise. Decide NOW: exclude, or route to a cold-start branch.
- Bots and staff don't just inflate error; they form their own segment. Ship a "4AM high-frequency buyer" segment and you've shipped your own QA team.

### Your levers this phase

- **Lever 1 (the big one): outlier handling.** Cap / log-transform / exclude / own-branch. This decision changes every downstream result. Retail default: log-transform spend variables; cap visits-per-week at 95th percentile.
- **Lever 2 (the sneaky one): contamination filters.** Bots, staff, test accounts, integration partners. Quantify BEFORE you fit.
- **Lever 3 (usually matters): missingness disposition.** Impute / drop / leave-as-NaN / flag with a mask feature. Each choice has different failure modes.
- **Lever 4 (only if large data): sampling.** Keep all / stratified subsample / weight by class. For tabular data <100k rows, usually keep all.
- **Skip unless specific:** schema normalisation (Phase 3's problem); feature derivation (Phase 3's problem).

### Trust-plane question

Is this data trustworthy? Which features are available at prediction time, leaky, or ethically loaded?

### Paste this

```
I'm entering Playbook Phase 2 — Data Audit. The scaffold pre-committed
to the dataset shape (5,000 customers × 14 features, 400 SKUs, 120,000
transactions under src/retail/data/arcadia_*.csv); my decision here is
the disposition per audit finding — cap, log-transform, exclude, flag,
or leave. I am not validating the data; I am deciding what to do with
what you find.

Copy journal/skeletons/phase_2_data_audit.md into
workspaces/metis/week-05-retail/journal/phase_2_data_audit.md. Fill
the blanks as we go; leave dispositions as TODO — those are my calls.

Run the six-category audit against the three CSVs under
src/retail/data/. For every finding in every category:

1. Duplicates — exact customer_id or transaction_id repeats. Report
   count + the customer_id / transaction_id of the first 3 offenders.
2. Contamination — staff, bot, test, or integration accounts. Cite
   the column and rule that flags them (e.g. "rows where email
   domain ends in @arcadia-internal.sg"). If the column doesn't
   exist, say so.
3. Sparsity — customers with fewer than 3 transactions. Report the
   count and the fraction.
4. Outliers — top-1% on any numeric feature (especially
   total_spend, visits_per_week). Report the threshold and count.
5. Labels-in-disguise — any column that is itself a pre-existing
   segment assignment, tier, or rule output (e.g. a legacy
   loyalty_tier column). Report column name + unique-value count.
6. Missingness — per-column NaN rate; flag any column >5% missing.

For every claim in the audit, cite the exact file and the specific
column or function you used — e.g. "from arcadia_customers.csv
column 'total_spend_sgd', or from customer_features() in
src/retail/backend/ml_context.py". If you cannot cite a file and a
column, delete the claim.

For every dollar figure you mention (if any), quote the line from
PRODUCT_BRIEF.md §2. The audit itself is not priced in dollars, but
the $45 wrong-segment and $3 touch costs come up if you describe the
business impact of skipping the audit.

Propose a disposition per finding — cap, log-transform, exclude,
flag, or leave — with a one-line reason each. I approve or overrule
per finding. Do NOT apply any disposition yet.

Do NOT use the word "blocker" unless you name the specific next phase
I cannot run. A 7% NaN rate on one column is a finding, not a blocker.

When the audit table is complete with cited findings and proposed
dispositions, stop and wait for me to approve per finding.
```

### Why this prompt is written this way

- Inheritance-framed opening names what the scaffold decided (dataset shape, CSV paths) and what's still mine (the disposition per finding) — this prevents the agent from proposing dispositions as facts.
- Cite-or-cut is tightened to "file + column or function" because data audit claims without a column citation are the #1 source of invented findings in Week 4.
- Six categories enumerated, each with a concrete what-to-report shape — prevents vague "everything looks fine" summaries that score 0 on rubric D3.
- Label-in-disguise gets its own numbered slot because in USML it's the difference between discovering structure and re-deriving the 2020 rulebook.
- "Do NOT apply any disposition yet" is load-bearing — the agent applying a log-transform before I approve corrupts the Phase 4 candidate sweep.

### What to expect back

- `journal/phase_2_data_audit.md` with findings filled in for all six categories and disposition blanks held as TODO.
- Per-category findings with counts and first-offender IDs, each cited to `src/retail/data/arcadia_*.csv` or a function in `src/retail/backend/ml_context.py`.
- A proposed disposition (cap / log / exclude / flag / leave) with a one-line reason per finding.
- A list of columns that look like pre-existing segment labels, if any exist.
- A stop signal pending per-finding approval.

### Push back if you see

- A finding without a column or function citation — "which file and which column produced this? please cite or delete."
- "The data looks fine" / "no major issues" without per-category evidence — "please walk through all six categories; each needs a count even if the count is 0."
- A disposition applied before my approval (e.g. "I log-transformed total_spend") — "please revert; dispositions are my call, not yours."
- A contamination rule without the column it runs on — "which column flags staff accounts? if no such column exists, say so."
- A dollar figure not quoted from `PRODUCT_BRIEF.md §2` — "please quote the §2 row."

### Adapt for your next domain

- Change `staff, bot, test, integration accounts` to the contamination pattern in your domain (QA testers, partner API calls, demo users).
- Change `legacy loyalty_tier column` to your domain's pre-existing rule output (risk tier, triage tier, severity band).
- Change `customers with <3 transactions` to your sparsity floor (sessions, encounters, orders).
- Change `top-1% on total_spend` to your domain's dominant-outlier signal.
- Change `arcadia_customers.csv` to your source dataset paths.

### Evaluation checklist

- [ ] All 6 audit categories addressed with specifics (row X, col Y, count Z).
- [ ] Outlier dispositions proposed (cap / log / exclude / own-branch) with a reason each.
- [ ] Singleton / low-observation customers flagged with a disposition.
- [ ] Label-in-disguise check run explicitly on every column that looks categorical or "tier"-shaped.
- [ ] Missingness disposition proposed per feature, not blanket.

### Journal schema — universal

```
Phase 2 — Data Audit
Accepted? Yes / Conditional / No
Conditions applied: ____
Known risks I am accepting: ____
Dispositions:
  Outliers: ____
  Singletons: ____
  Missingness: ____
  Contamination: ____
  Label-in-disguise candidates: ____
```

### Common failure modes

- Audit output accepted as-is; no call made on any of the six categories — scores 1/4 on D3.
- "Everything looks fine" without specifics — the phase did not happen.
- Singleton customers left in for clustering — they become a noise cluster that pollutes every segment's boundary.

### Artefact

`workspaces/.../journal/phase_2_data_audit.md`

### Instructor pause point

- Show a scatter of two RFM features with top-1% left in vs removed. Ask: which picture is the segmentation going to be _about_?
- Raise-hands: who would exclude the top 1% of spenders from the segmentation? Who would keep them _in_ but in their own segment? Debate 2 minutes.
- Ask: what's a label-in-disguise column in your industry? (Credit: "risk tier." Hospital: "DRG code." Retail: "loyalty tier.") If you can't answer, you haven't audited.

### Transfer to your next project

1. Which populations are contaminating the dataset (bots, staff, test, integration) and have I quantified them BEFORE I fit anything?
2. Is there a field that is a leftover label from an older rule-based system — and if I leave it in, will my model simply re-derive the thing my buyer is paying me to replace?
3. What is my plan for rare-but-real outliers — cap, log, exclude, or own-branch — and have I written the plan down BEFORE I saw the model output?

---

