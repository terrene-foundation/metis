<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 6 — Sprint 4 MLOps Boot (drift monitoring × 3 models)

> **What this step does:** Boot Sprint 4 by copying the drift skeleton, confirming the drift status endpoint, and orienting Claude Code on the three-separate-rules requirement — before Phase 13 fires.
> **Why it exists:** The most common Sprint 4 failure is writing one combined drift rule for all three models. The boot makes this failure explicit up front: different models drift on different signals at different cadences, and a single alarm doesn't work.
> **You're here because:** Phase 12 postpdpa was written and the LP plan was re-solved with the PDPA hard constraint. Sprint 3 is complete.
> **Key concepts you'll see:** variance-grounded threshold, signal-per-model, seasonal exclusion, HITL disposition, retrain authority

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering an MLOps sprint. The scaffold pre-registered drift reference
data on my behalf. My job this sprint is to set retrain rules — one per
model — because different models drift on different signals at different
cadences. A single alarm watching all models is not an acceptable rule.

This sprint runs the drift monitoring phase once per model, producing one
journal entry with separate sub-sections — not separate files.

Before the phase walk:

1. Copy the sprint skeleton from journal/skeletons/ into journal/.

2. Confirm the drift endpoint is live by checking the reference registration
   status. If the reference is not registered, STOP and raise a hand —
   do NOT attempt to re-seed the reference; that is the scaffold's job.

3. For every drift signal you name (population shift, stability score,
   calibration error, constraint-violation rate), cite the file and function
   in the codebase that computes it. If you cannot cite, say so.

4. I will ground every threshold in historical variance, not in round numbers.
   If you propose a threshold without a variance grounding, the rule is
   post-hoc. Run the relevant drift check endpoints and report the observed
   variance so I can ground my thresholds in it.

5. Do NOT propose the thresholds, duration windows, or HITL dispositions for
   any rule. Those are my calls.

6. Do NOT use "auto-retrain" phrasing. Retrain is a human decision on signal;
   the monitoring system reports, the human pulls the trigger.

7. Do NOT use the word "blocker" without naming a specific action.

Once skeleton is copied and endpoint confirmed, summarise: (a) the models
covered and the signal each uses, (b) the check windows you will run and
the variance each returns, (c) the rubric row for this phase.

Then stop and wait for my Phase 13 prompt.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
Sprint: Sprint 4 MLOps — drift monitoring × 3 models.
Phase covered: Phase 13 × 3. One journal entry — phase_13_retrain.md —
with three sub-sections. NOT three separate files.

Skeleton copy: phase_13_retrain.md from journal/skeletons/. One file.
See journal/skeletons/README.md.

Endpoint check (GET only):
- /drift/status/customer_segmentation → should return "reference_set": true
If not true, STOP and raise a hand — do NOT attempt to re-seed the
drift reference.

The three rules, by model and signal:
- Segmentation (USML): monthly segment-membership churn.
  Signal: what fraction of customers changed segments month-to-month.
  One customer changing is noise; 10% changing is drift.
- Churn classifier (SML): weekly calibration error + AUC decay.
  A classifier can have stable AUC and drifted calibration; both matter
  because Sprint 3's allocator consumes the probability directly.
- Allocator (Opt): daily constraint-violation rate + feasibility rate.
  If the LP starts producing infeasible plans or ops overrides them,
  something upstream broke.

Drift check endpoints — run BOTH windows and report observed variance:
- /drift/check?window=recent_30d
- /drift/check?window=catalog_drift

Variance grounding is mandatory for D5. "15% because the rolling-weekly
variance has its 95th percentile at 12%" scores 4/4. "15% because it
feels big" scores 1/4.

Seasonal exclusion: Nov–Dec (Black Friday / Year-End) is explicitly
excluded from the segmentation baseline per PRODUCT_BRIEF.md §2.
Peak-season spikes are seasonality, not drift — quote the line.

Do NOT use "auto-retrain" phrasing. Retrain is a human decision.

Summary must name: (a) three rules × signals × cadences,
(b) two drift check windows and observed variance,
(c) D5 rubric row: signal + threshold + duration window + HITL +
seasonal exclusion = 4/4.

Then stop and wait for my Phase 13 prompt.
```

**How to paste:** Combine both blocks into a single paste into your `claude` session.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ One skeleton file copied: `journal/phase_13_retrain.md`
- ✓ `/drift/status/customer_segmentation` returned `"reference_set": true`
- ✓ Two drift check runs: `recent_30d` and `catalog_drift`, each returning observed variance
- ✓ Summary names three rules × signals × cadences (separate, not combined)
- ✓ D5 rubric row stated: signal + threshold + duration window + HITL + seasonal exclusion
- ✓ No proposed thresholds, no "auto-retrain" phrasing
- ✓ Stop signal pending the Phase 13 prompt
- ✓ Viewer (http://localhost:3000) refreshes and shows: Sprint 4 tile activates; drift-report region is visible

**Signals of drift — push back if you see:**

- ✗ A single combined rule ("retrain when any of the three signals fires") — ask "don't the three models have different cadences? Please separate."
- ✗ A proposed threshold without variance grounding — ask "what's the 95th-percentile of historical variance for this signal? Ground the number or remove it."
- ✗ "Auto-retrain" phrasing — ask "who pulls the retrain trigger — the system or me? Please re-frame as signal → operator."
- ✗ Missing Nov–Dec exclusion — ask "does this rule exclude peak season? Please quote the `PRODUCT_BRIEF.md §2` Nov–Dec line."
- ✗ An attempt to re-register the drift reference — ask "isn't the reference already registered by the scaffold? Please don't re-seed; check `/drift/status/customer_segmentation` again."
- ✗ Viewer Sprint 4 tile does not activate — confirm `/drift/status/customer_segmentation` GET ran and returned `"reference_set": true`.

---

## 3. Things you might not understand in this step

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Variance-grounded threshold** — a retrain rule whose trigger value is derived from historical measurement, not chosen arbitrarily
- **Signal-per-model** — the principle that each model type drifts differently and needs its own alert, not a shared one
- **Seasonal exclusion** — explicitly excluding known seasonal patterns so they don't trigger false retrains
- **HITL disposition** — whether the retrain trigger requires a human decision or can be automated (and why human is the default here)
- **Retrain authority** — who has the right to pull the retrain trigger, and why it's not the monitoring system

---

## 4. Quick reference (30 sec, generic)

### Variance-grounded threshold

A retrain threshold derived from historical measurement. Instead of "retrain when segment churn exceeds 15%," you look at the historical rolling variance of segment churn and set the threshold at, say, the 95th percentile of that distribution. This is grounded: the number comes from the data, not from a guess. The D5 rubric rewards grounded thresholds (4/4) and penalises round-number guesses (1/4) because round numbers are usually arbitrary and fail in production — either they're too sensitive (constant false alarms) or too loose (real drift slips through).

> **Deeper treatment:** [appendix/06-monitoring/retrain-rules.md](./appendix/06-monitoring/retrain-rules.md)

### Signal-per-model

Each model type drifts differently: unsupervised segmentation drifts when customer behaviour shifts (monthly); classifiers drift when the relationship between features and outcomes changes (weekly calibration check); optimisation models drift when their inputs become infeasible or their plans get overridden (daily check). A single "drift alarm" set at a round threshold watching all three simultaneously either fires constantly (too sensitive) or catches nothing (too loose). One rule per model, tuned to that model's cadence and signal, is the operational contract.

> **Deeper treatment:** [appendix/06-monitoring/drift-types.md](./appendix/06-monitoring/drift-types.md)

### Seasonal exclusion

Explicitly removing known seasonal patterns from the drift baseline so they don't trigger false retrains. For Arcadia, Nov–Dec Black Friday and Year-End traffic are expected spikes — they look like drift (volume doubles, mix shifts) but they are predictable seasonality. Including Nov–Dec in the baseline produces a reference that averages across the spike, making every non-peak month look like it has drifted downward. The seasonal exclusion is cited from `PRODUCT_BRIEF.md §2` so it's documented and auditable.

> **Deeper treatment:** [appendix/06-monitoring/segment-membership-churn.md](./appendix/06-monitoring/segment-membership-churn.md)

### HITL disposition

Human-in-the-loop (HITL) disposition means the monitoring system raises a signal and a human decides whether to retrain — the system does not retrain automatically. Tonight, retrain is always HITL. Why: automated retrain on a false alarm retrains the model on noisy data and can silently degrade performance. A human reviewing the signal can distinguish "this is real drift" from "this is a seasonal spike" or "this is a data-pipeline anomaly." The monitoring system's job is to report; the decision authority belongs to the operator.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

### Retrain authority

The explicit assignment of who can pull the retrain trigger. Tonight that is the operator (you, or the marketing data team), not the monitoring system. "Auto-retrain when AUC drops 3 points" removes human judgment from a decision that may affect live campaign budgets. Retrain authority matters because retraining the segmentation model changes which customers are in which segment, which changes the allocator plan, which changes how $X,000 of campaign budget is distributed. That is not a decision for an alarm to make unilaterally.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in the Sprint 4
MLOps boot step.

Read `workspaces/metis/week-05-retail/playbook/workflow-06-sprint-4-mlops-boot.md`
for what this step does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. variance-grounded threshold >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in the Sprint 4 boot
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] `journal/phase_13_retrain.md` skeleton exists
- [ ] `/drift/status/customer_segmentation` returned `"reference_set": true`
- [ ] Both drift check windows run (`recent_30d` and `catalog_drift`) with observed variance reported
- [ ] Summary covers three separate rules × signals × cadences; D5 rubric row stated
- [ ] No proposed thresholds; no auto-retrain phrasing
- [ ] Claude Code has stopped and is waiting for the Phase 13 prompt

**Next file:** [`phase-13-drift.md`](./phase-13-drift.md)
