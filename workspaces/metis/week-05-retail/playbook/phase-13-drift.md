<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 13 — Drift Monitoring

> **What this phase does:** Set one retrain rule per deployed model — three rules tonight, one for each of segmentation, churn classifier, and allocator — each grounded in historical variance with a human-in-the-loop disposition and a seasonal exclusion.
> **Why it exists:** Without a written rule, "monitor for drift" means nothing. A rule names the signal, the variance-grounded threshold, the duration window, and who decides to retrain — before anything drifts.
> **You're here because:** Sprint 4 just booted (`workflow-06-sprint-4-mlops-boot.md`). Phase 13 produces the three retrain rules before you hand off to red-team.
> **Key concepts you'll see:** drift signal types, segment-membership churn, calibration decay, constraint-violation rate, variance-grounded thresholds, HITL on first trigger, seasonal exclusion

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Playbook Phase 13 — Drift Monitoring. My decision
here is THREE RETRAIN RULES — one per deployed model. Not one
rule for all models; three separate rules with separate signals,
separate cadences, and separate duration windows. I set the
threshold values; you draft the rule shapes and the observed
variance so I can ground my numbers.

Your job:

1. Confirm the drift reference is registered for each deployed
   model. Run the drift-status check for each. If any shows
   "reference_set": false, STOP and flag it — do NOT attempt
   to re-seed; that is the scaffold's responsibility.

2. Run the drift check against two windows (recent and
   scenario-inject if provided). Report the OBSERVED VARIANCE
   per signal: 50th, 95th, and 99th percentile of historical
   variance. I need these three numbers to ground my thresholds.

3. Draft the SHAPE of three rules — one per model — each with:
   - Signal(s): named per model (not one combined signal)
   - Cadence: named per model (not one combined cadence)
   - Threshold grounding: "to be set by the student at the
     95th percentile of observed variance from step 2"
   - Duration window: named per model with a rationale —
     distinguish one-day anomaly from genuine multi-day drift
   - HITL disposition: first trigger is ALWAYS human-in-the-
     loop. After multiple consecutive clean retrains, the
     operator may opt into auto-retrain — but the default is
     HITL. Do NOT write "auto-retrain when X > Y"; write
     "signal fires → operator decides to retrain or hold"
   - Seasonal exclusion: quote the known seasonality window
     from the project's brief verbatim. Peak-season spikes
     are seasonality, not drift — the duration window and
     HITL disposition prevent retraining on them

4. Cite the drift signal functions in the codebase. For every
   signal (PSI, membership stability measure, calibration
   score, constraint-violation rate), name the function. If
   you cannot cite, say so.

Do NOT propose THRESHOLD VALUES. The numbers are mine, grounded
in the observed variance you reported in step 2.

Do NOT write "auto-retrain when X > Y" anywhere in the rules.
Retrain is a human decision. Reframe any auto-retrain language
as "signal fires → operator decides".

Do NOT POST the retrain rules until I approve each one.

When reference confirmed, observed-variance table populated, and
three rule shapes drafted, stop and wait for me to write the
threshold values.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
Three models, three rules, one journal file.
Journal file: copy journal/skeletons/phase_13_retrain.md into
  workspaces/metis/week-05-retail/journal/phase_13_retrain.md.
Drift endpoints per src/retail/backend/routes/drift.py:
  - GET /drift/status/{model_id}
  - POST /drift/check
  - POST /drift/retrain_rule

The three models and their drift shapes:

1. Segmentation (model_id: customer_segmentation)
   Signal: segment-membership churn — fraction of customers
     who move segments month-over-month.
   Cadence: MONTHLY (segmentation re-scores monthly).
   Duration window: 2 consecutive monthly triggers = real drift;
     1 trigger = possible seasonality or sampling variance.
   Variance grounding: run /drift/check with recent_30d window;
     report 50th / 95th / 99th percentile of membership churn.

2. Churn classifier (model_id: churn)
   Signals: calibration error (Brier score rolling) + AUC decay
     + feature PSI (top 5 features).
   Cadence: WEEKLY.
   Duration window: 1 week = investigate; 3 consecutive weeks
     = retrain candidate.
   Variance grounding: run /drift/check with recent_30d window;
     report observed variance per signal.

3. Conversion classifier (model_id: conversion)
   Signals: same as churn classifier — Brier + AUC + feature PSI.
   Cadence: WEEKLY.
   Duration window: same as churn classifier.

(Allocator drift monitoring, if applicable):
   Signal: constraint-violation rate + feasibility rate.
   Cadence: DAILY (allocator re-solves daily).
   Duration window: 3 consecutive daily triggers = pattern;
     1 trigger = likely data anomaly.

Seasonal exclusion — quote from PRODUCT_BRIEF.md §2 verbatim:
  the Nov–Dec (Black Friday / Year-End) row. Peak-season spikes
  during this window are known seasonality — the rules must
  exclude them from automatic retrain triggers.

Run /drift/check against two windows:
  - recent_30d
  - catalog_drift (src/retail/data/scenarios/catalog_drift.json)
Report 50th / 95th / 99th percentile of observed variance per
  signal from both windows.

Do NOT attempt to re-register drift reference data. If
  "reference_set" is false for any model, flag it — that is a
  scaffold issue, not a Phase 13 issue.

Do NOT POST /drift/retrain_rule until I write the threshold
  values and approve each rule.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `journal/phase_13_retrain.md` exists with three separate rule skeletons — one each for segmentation, churn classifier, and (conversion classifier or allocator)
- ✓ Observed-variance table present: 50th / 95th / 99th percentile per signal, from both `/drift/check` windows
- ✓ `"reference_set": true` confirmed for each model — if any is false, it is flagged, not worked around
- ✓ Each rule has a named signal, cadence, duration window with a rationale, HITL disposition, and seasonal exclusion
- ✓ Nov–Dec seasonal exclusion quoted verbatim from `PRODUCT_BRIEF.md §2`
- ✓ Every signal cited to a function in `src/retail/backend/routes/drift.py` — or explicitly "cannot cite"
- ✓ No threshold values in the rule shapes — those are blank for you to fill from the variance table
- ✓ Stop signal waiting for you to write threshold values and approve
- ✓ Viewer (http://localhost:3000) shows: drift-monitor panel with three rule cards (one per model) — each card showing signal, cadence, duration window, HITL flag, and seasonal-exclusion marker

**Signals of drift — push back if you see:**

- ✗ One combined drift rule for all three models — "the three models have different signals and cadences; please split into three separate rules"
- ✗ A proposed threshold value ("15% membership churn") — "please remove; I write the values grounded in the observed variance you reported"
- ✗ "Auto-retrain when X > Y" anywhere — "please reframe as 'signal fires → operator decides'; retrain is a human call"
- ✗ An attempt to re-register drift reference data — "if reference_set is false, that is a scaffold issue; flag it and stop"
- ✗ Missing Nov–Dec exclusion — "please quote the §2 Nov–Dec row; peak-season spikes are seasonality, not drift"
- ✗ Viewer shows nothing new after CC reports the phase complete — CC may have described the rules without posting them. Re-prompt: "show me the drift-monitor panel; are all three rule cards visible?"

---

## 3. Things you might not understand in this phase

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Drift signal types** — the different measurable signals that indicate a model's world is changing: input-feature distributions (PSI), output quality (AUC decay, Brier score), cluster stability (membership churn), and operational feasibility (constraint-violation rate)
- **Segment-membership churn** — for a segmentation model, the fraction of customers who move from one segment to another month-over-month; high churn means the segments are unstable or the customer base is genuinely shifting
- **Calibration decay** — a classifier's predicted probabilities drifting away from actual outcome rates; a model can have stable AUC (it still ranks correctly) but broken calibration (its probabilities are wrong in dollar terms)
- **Constraint-violation rate** — for the allocator, the fraction of days the solved plan violates one or more soft constraints; rising violation rate means the business environment is drifting away from the constraint assumptions
- **Variance-grounded thresholds** — setting a retrain trigger at the 95th percentile of observed historical variance, not a round number; this ensures the alarm fires on genuine outlier drift, not normal fluctuation
- **HITL on first trigger** — the rule that the first time a drift signal fires, a human must decide whether to retrain; the monitor reports, the operator decides; auto-retrain is only permitted after multiple stable retrain cycles
- **Seasonal exclusion** — a time window (Nov–Dec for Arcadia) where known spikes happen that look like drift but are actually calendar effects; rules must exclude this window from automatic triggers

---

## 4. Quick reference (30 sec, generic)

### Drift signal types

Four types tonight: (1) Feature PSI — are the input distributions shifting? (2) Performance decay — is AUC or Brier score dropping? (3) Membership churn — for segmentation, are customers moving between segments at unusual rates? (4) Constraint-violation rate — for the allocator, are the operational constraints being breached more often? Each model has its own primary signal; a single combined alarm misses the differences in cadence and urgency between them.

> **Deeper treatment:** [appendix/06-monitoring/drift-types.md](./appendix/06-monitoring/drift-types.md)

### Segment-membership churn

Each month, some customers who were in segment A will be in segment B. A healthy segmentation has a stable monthly churn rate — say 5–10%. A 30% monthly rate means either the segments are unstable (bad K choice or poor features) or the customer base genuinely shifted (an external shock, a new competitor, a platform algorithm change). Monitoring this rate catches the difference between model decay and genuine business change. Tonight: the drift-check reports membership churn across two windows; the 95th percentile of historical variance is the threshold anchor.

> **Deeper treatment:** [appendix/06-monitoring/segment-membership-churn.md](./appendix/06-monitoring/segment-membership-churn.md)

### Calibration decay

Calibration measures whether a classifier's probabilities match actual outcomes. A well-calibrated model that says 30% churn probability should see 30% of those customers churn in practice. Calibration can decay independently of AUC — the model still ranks customers in the right order (AUC stable) but its probability estimates drift (Brier score rises). In dollar terms this matters: the allocator uses these probabilities to compute expected revenue. A drifted Brier score means the allocation is based on wrong revenue estimates even if rankings look fine.

> **Deeper treatment:** [appendix/06-monitoring/calibration-decay.md](./appendix/06-monitoring/calibration-decay.md)

### Variance-grounded thresholds

A threshold set at a round number ("flag when drift > 15%") is almost always wrong — either too sensitive (fires on normal fluctuation, causing alert fatigue) or too loose (misses real drift). A variance-grounded threshold is set at the 95th percentile of observed historical variance for that signal. If the historical 95th percentile of weekly membership churn is 12%, the threshold becomes 13–15% — slightly above the tail, not a guess. Tonight: the observed-variance table from the drift-check windows gives you the 50th, 95th, and 99th percentile; you set the threshold from those numbers.

> **Deeper treatment:** [appendix/06-monitoring/retrain-rules.md](./appendix/06-monitoring/retrain-rules.md)

### HITL on first trigger

Human-in-the-loop on the first retrain trigger. When a drift signal first crosses the threshold, the monitoring system reports it — and a human decides whether to retrain. The human checks: is this genuine drift or a one-off anomaly or known seasonality? Only after the human confirms genuine drift does retraining happen. After multiple clean retrain cycles (the process has been reliable), the operator may choose to auto-retrain on future triggers. The default is always HITL — auto-retrain is an opt-in after proven reliability.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

### Seasonal exclusion

A calendar window — Nov–Dec for Arcadia — where known events (Black Friday, Year-End sales) produce spikes in customer behaviour that look like model drift but are actually planned seasonality. Without a seasonal exclusion, the drift monitor fires during Black Friday and triggers a retrain on data that is intentionally abnormal. The retrained model is then worse for the 50 weeks after it. The seasonal exclusion says "ignore triggers in this window; check again in January." Tonight: quote the Nov–Dec row from `PRODUCT_BRIEF.md §2` verbatim as the exclusion anchor.

> **Deeper treatment:** [appendix/06-monitoring/retrain-rules.md](./appendix/06-monitoring/retrain-rules.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in Playbook
Phase 13 — Drift Monitoring.

Read `workspaces/metis/week-05-retail/playbook/phase-13-drift.md` for
what this phase does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. variance-grounded thresholds >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in Phase 13
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] `journal/phase_13_retrain.md` exists with three separate rule skeletons — one for each deployed model
- [ ] Observed-variance table present with 50th / 95th / 99th percentile per signal from both drift-check windows
- [ ] `"reference_set": true` confirmed for each model (or scaffold issue flagged if false)
- [ ] Every rule has: signal, cadence, duration window + rationale, HITL disposition, seasonal exclusion
- [ ] Nov–Dec exclusion quoted verbatim from `PRODUCT_BRIEF.md §2`
- [ ] No auto-retrain language anywhere — "signal fires → operator decides" throughout
- [ ] You approved each rule and provided threshold values before `/drift/retrain_rule` was POSTed
- [ ] Viewer drift-monitor panel shows three rule cards, each with signal, cadence, HITL flag, and seasonal-exclusion marker

**Next file:** [`workflow-07-redteam.md`](./workflow-07-redteam.md)

Phase 13 completes Sprint 4. The final red-team runs next, covering all four sprints.
