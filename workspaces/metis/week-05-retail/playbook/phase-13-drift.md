<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Phase 13 — Drift (× 3 models tonight)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ USML ✓ ▸ SML ✓ ▸ Opt ✓ ▸ **MLOps ◉** ▸ Close
 THIS PHASE:    Sprint 4 · Phase 13 of 14 — Drift Monitoring
 LEVERS:        signal choice · threshold grounding · duration window · HITL-vs-auto
──────────────────────────────────────────────────────────────────
```

### Concept

Setting up monitoring for the day after launch. Reference data registered; current-week data checked. You propose signals and thresholds grounded in historical variance, classify each rule as human-in-the-loop or automatic. The retrain decision stays in the Trust Plane; the monitoring system reports signals, it does not pull the trigger.

**Three models tonight, three drift rules.** Segmentation (USML) drifts on **membership churn** — fraction of customers who move segments monthly. Churn classifier (SML) drifts on **calibration decay + feature PSI**. Allocator (Opt) drifts on **constraint-violation rate + feasibility rate**. Not one alarm — three, with separate cadences.

### Why it matters (SML + USML + Opt lenses — the DEPTH Week 4 skipped)

- **Feature drift (PSI)** measures distributional shift in input features. PSI < 0.1 stable, 0.1–0.25 moderate, > 0.25 severe.
- **Performance decay** measures target-related drift. For SML: AUC decay, precision decay, recall decay. For USML: cluster-stability decay (re-cluster + compare).
- **Calibration drift** measures whether predicted probabilities still match actual rates. A classifier can have stable AUC and drifted calibration.
- **Concept drift** (label definition changes over time) is the subtlest. If "churn" means "90 days of inactivity" today and will mean "60 days" next year, your label is moving. Monitor your definitions.
- **Virtuous drift** (the model got better!) is also drift. If your customer base is maturing and the old threshold is too sensitive, the model needs retraining to benefit from the shift — not just when it degrades.
- **Don't retrain on seasonal spikes.** Black Friday, Chinese New Year, payday. These look like drift but are known seasonality. Duration window + HITL on first trigger.

### Your levers this phase

- **Lever 1 (the big one): signal choice per model.** Segmentation = membership churn %. Classifier = calibration error + AUC decay + feature PSI. Allocator = constraint-violation rate.
- **Lever 2 (threshold grounding):** historical rolling variance, not round numbers. "0.15 because it's the 95th percentile of weekly drift variance in the past year" = 4/4. "0.15 because that's sort of big" = 1/4.
- **Lever 3 (duration window):** 1 day of drift = usually seasonality or single-day anomaly. 7 days = real. 30 days = definitely. Pick based on the cost of a false-positive retrain.
- **Lever 4 (HITL vs auto):** first trigger always HITL (human approves). Repeat triggers may auto-retrain if the process has been stable for multiple cycles.

### Trust-plane question

When do we retrain? What is the rule?

### Paste this

```
I'm entering Playbook Phase 13 — Drift. The scaffold pre-committed
to drift reference data registered at startup and the endpoints
/drift/status/{model_id}, /drift/check, /drift/retrain_rule per
src/retail/backend/routes/drift.py; my decision here is THREE
RETRAIN RULES — one per model, grounded in historical variance,
with human-in-the-loop disposition. Not one rule for three models;
three rules, three cadences.

Copy journal/skeletons/phase_13_retrain.md into
workspaces/metis/week-05-retail/journal/phase_13_retrain.md.

Your job:

1. Confirm the drift reference is registered for each of the
   three models:
   - Segmentation (customer_segmentation)
   - Churn classifier (churn)
   - Conversion classifier (conversion)
   Run GET /drift/status/customer_segmentation and confirm
   "reference_set": true. If not, STOP — do NOT attempt to
   re-seed; that is the scaffold's responsibility.

2. Run /drift/check against two windows — recent_30d AND
   catalog_drift (per src/retail/data/scenarios/
   catalog_drift.json). Report the OBSERVED VARIANCE per signal.
   I need the 50th, 95th, 99th percentile of the historical
   variance to ground my thresholds in.

3. Draft the SHAPE of three rules — one per model — each with:
   - Signal(s): segmentation = membership churn; churn
     classifier = calibration error + AUC decay + feature
     PSI; conversion classifier = same; allocator (if
     applicable) = constraint-violation rate.
   - Cadence: segmentation monthly; classifiers weekly;
     allocator daily.
   - Threshold grounding: "to be set by the student at the
     95th percentile of observed variance from step 2".
   - Duration window: 1 day is seasonality, 7 days is real,
     30 days is definitive. Segmentation needs 2 consecutive
     triggers; classifier needs 1; allocator needs 3. Name
     the rationale.
   - HITL disposition: first trigger is ALWAYS human-in-the-
     loop. After 3 consecutive clean re-trains, the operator
     may opt into auto-retrain — but the default is HITL.
   - Seasonal exclusions: quote PRODUCT_BRIEF.md §2 Nov–Dec
     (Black Friday / Year-End) row verbatim. Peak season is
     seasonality, not drift.

4. Cite the drift signal functions in src/retail/backend/
   routes/drift.py. For every signal (PSI, Jaccard, Brier,
   constraint-violation rate), name the function. If you cannot
   cite, say so.

Do NOT propose THRESHOLD VALUES. I write the numbers grounded in
the observed variance you reported in step 2. A threshold you
proposed that happens to match the 95th percentile is still
post-hoc — the discipline is that I set the number.

Do NOT use "auto-retrain when X" phrasing. Retrain is a human
decision. The monitor reports; the operator pulls. Reframe any
"auto-retrain" as "signal fires → operator decides".

Do NOT POST /drift/retrain_rule until I approve per rule. The
classifications are my call.

Any dollar figure cited — including any §2 cost (e.g. $45 for
wrong-segment, driving the segmentation drift urgency) — must be
quoted verbatim from §2. Drift thresholds themselves are
variance-grounded (not $-grounded), but any downstream dollar
claim ("below this threshold, the wrong-segment cost climbs
above $X/month") must be §2-sourced.

Do NOT use "blocker" without naming the specific ship-action.

When the reference is confirmed registered, the observed-variance
table is populated from both windows, and the three rule shapes
are drafted with cadence / HITL / seasonal exclusion, stop and
wait for me to write the threshold values.
```

### Why this prompt is written this way

- Inheritance-framed opening names the scaffold's drift reference and endpoints and keeps the three threshold values with me — three rules, three cadences is the load-bearing structural insight.
- Variance-grounded thresholds are required with explicit percentile language so the agent reports variance rather than picking a round number.
- "Do NOT attempt to re-seed" is the load-bearing anti-trap from Phase 13 common failure #1 — re-seeding masks a scaffold issue as a drift problem.
- No-auto-retrain phrasing enforces the `.claude/rules/agent-reasoning.md` principle that retrain stays with the human — monitor reports, operator pulls.
- Show-the-brief on Nov–Dec seasonal exclusion is mandatory because without it the first Black Friday spike triggers a retrain on known seasonality.

### What to expect back

- `journal/phase_13_retrain.md` with three rule skeletons (segmentation / churn / conversion).
- An observed-variance table with 50th / 95th / 99th percentile per signal from the two `/drift/check` windows.
- `"reference_set": true` confirmations for each model.
- Every signal cited to a function in `src/retail/backend/routes/drift.py`.
- A quoted Nov–Dec seasonal exclusion line from `PRODUCT_BRIEF.md §2`.
- A stop signal pending my threshold values.

### Push back if you see

- A proposed threshold value ("15% membership churn") — "please remove; I write the values from the observed variance you reported."
- "Auto-retrain when X > Y" phrasing — "please reframe as 'signal fires → operator decides'. retrain is a human call."
- One combined rule for three models — "the three models have different cadences; please split into three rules."
- An attempt to re-register drift reference data — "please don't re-seed; if `reference_set` is false, that's a scaffold issue — hand up instead."
- Missing Nov–Dec exclusion — "please quote the §2 Nov–Dec row; peak-season spikes are seasonality, not drift."

### Adapt for your next domain

- Change the three models (segmentation / churn / conversion) to your domain's deployed artefacts.
- Change `PSI / Jaccard / Brier / constraint-violation rate` signals to your domain's drift signals.
- Change `Nov–Dec Black Friday` to your domain's known seasonality window.
- Change `monthly / weekly / daily` cadences to match your models' observable drift timescales.
- Change `/drift/status/{model_id}` etc. to your domain's drift endpoints.

### Evaluation checklist

- [ ] Reference data confirmed registered for every model.
- [ ] Primary + secondary signals named per model.
- [ ] Thresholds grounded in historical variance, not round numbers.
- [ ] Duration window prevents retrain-on-spike.
- [ ] HITL-vs-auto classified with reason.
- [ ] Retrain decision stays in Trust Plane (no "auto-retrain on X" without HITL first).

### Journal schema — universal

```
Phase 13 — Retrain Rule (per model)
Model: ____
Signal(s): ____
Threshold(s): ____ (variance grounding: ____)
Duration window: ____
Human-in-the-loop: yes / no (justification: ____)
Seasonal exclusions: ____
Reversal: what makes me change this rule? ____
```

### Common failure modes

- `set_reference_data` not called — drift check returns "no reference".
- Threshold = "15% feels right" without variance grounding — 1/4 on D5.
- Duration window = "immediately" — model retrains on Black Friday → produces worse model.
- Agent-reasoning violation: "auto-retrain when X > Y". Must be reframed as "signal + threshold for operator" — the human owns retraining.
- Single rule for all three models — the cadences are different, the signals are different, the rule must be different.

### Artefact

`POST /drift/retrain_rule` × 3 + `journal/phase_13_retrain.md`.

### Instructor pause point

- Ask: if segment-reassignment rate was 8% last month and 14% this month, is that drift? What's the fourth data point that turns "two spikes" into "a trend"?
- Draw two cadences (segmentation monthly, recommender daily). What would a single combined alarm miss on each side?
- Show a Black-Friday-shaped data spike. Ask: retrain or hold? Why?

### Transfer to your next project

1. What is the signal my product leaks when it starts going wrong — and is there a measurable historical baseline for what "normal" looks like?
2. What duration distinguishes genuine drift from known seasonality or one-off spikes?
3. Who decides to retrain — human with signal as input, or automatic? If automatic, what's my safeguard against retraining on a Black-Friday-style event?

---

