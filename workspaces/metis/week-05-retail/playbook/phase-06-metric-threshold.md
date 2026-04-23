<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Phase 6 — Metric + Threshold (REPLACED for USML)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 6 of 8 — Metric + Threshold (USML)
 LEVERS:        primary metric · threshold · class imbalance · calibration
──────────────────────────────────────────────────────────────────
```

### Concept

When there is no label, there is no single accuracy number to optimise. This phase replaces Week 4's "pick the metric, pick the threshold, tie to dollars" with a **three-floor commitment**: separation floor, stability floor, business-actionability floor. All three declared BEFORE you see the leaderboard. You pick the K that clears all three and maximises dollar lift versus the incumbent rule-based system.

**What's different from Week 4.** Week 4 asked "which accuracy metric, which threshold, tied to what costs?" and the answer was MAPE plus a conservative/moderate/aggressive interval with dollar cost per bucket. Week 5 has no MAPE. The conversation becomes **commit to floors** (pre-registration), not **optimise one number**. Dollar linkage is a **counterfactual vs the current rule-based system**, not raw cost-of-error.

### Why it matters (SML lens)

- Reinforces Week 4's metric-cost linkage: the leaderboard number only earns its keep when translated to dollars per month.
- Reinforces Week 3's cost-asymmetry logic — $45 wrong-segment and $18 converted-recommendation are the two sides of retail's ledger, mirroring $40/$1 fraud asymmetry.
- Reinforces Week 2/3's pre-registration rule: thresholds set AFTER seeing results are always conveniently where the leader landed. Cheating yourself.

### Why it matters (USML lens)

- **Separation** (silhouette or Davies-Bouldin) = how crisp are the clusters. Ship-by-separation-alone → segmentations that dissolve in two months.
- **Stability** (bootstrap Jaccard) = what fraction of customers stay in the same pair when you re-cluster on a different month or a different seed. Convention: 0.80 floor.
- **Actionability** = can marketing build a DISTINCT campaign for each segment? Not a number, a test. If two segments get the same one-line action, they are one segment with noise — collapse them.
- **Dollar lift via counterfactual** — not "how much does each error cost" but "how many fewer customers does this K send to the wrong campaign ($45 saved each) and how many more convertible clicks ($18 gained each) vs the 2020 rulebook." That's what turns a floor into a business case.

### Your levers this phase

- **Lever 1 (the big one): the three floors, pre-registered.** Separation floor (silhouette ≥ 0.25 is a typical minimum for real data), stability floor (Jaccard ≥ 0.80), actionability floor (one distinct campaign per segment — tested by naming). Declare BEFORE you see Phase 4 leaderboard.
- **Lever 2 (the business anchor): dollar counterfactual.** How many customers does this K re-route to a better campaign vs the rulebook? Multiply by $45.
- **Lever 3 (the reversal condition): what drops you back to the baseline?** "If stability drops below 0.80 on next month's re-cluster for two consecutive re-clusters, drop back to K-1."
- **Lever 4 (only for SML replay): class imbalance + calibration.** Not applicable to USML (no class).

### Trust-plane question

Which floors, at what values, tied to what dollar lift versus the incumbent?

### Paste this

```
I'm entering Playbook Phase 6 — Metric + Threshold. The scaffold
pre-committed to the shape of the commitment (three-floor
pre-registration for USML, PR-curve + calibration for SML); my
decision here is the FLOORS and the THRESHOLD — and I am
pre-registering them in writing BEFORE we re-open the leaderboard.

Which sprint am I in?
- Sprint 1 USML → I pre-register THREE floors (separation,
  stability, actionability). Skeleton:
  journal/skeletons/phase_6_metric_threshold.md → write
  journal/phase_6_usml.md.
- Sprint 2 SML → I pre-register a THRESHOLD-SELECTION RULE on the
  PR curve AND a Brier-score calibration floor. Write
  journal/phase_6_sml.md (same skeleton).

Here is how I want you to help me pre-register — I am the one
writing the values. You:

1. First, CONFIRM that you have not yet reopened the Phase 4
   leaderboard. If you have already seen the winning K or the
   winning family in the last two messages, say so — we must
   record that the floors were set post-hoc and treat the rubric
   accordingly. Honesty first; do not conceal the order.

2. USML path — draft the three floor definitions (NOT values) in
   the journal:
   (a) Separation floor — silhouette (or equivalent) measured how?
   (b) Stability floor — bootstrap Jaccard over how many re-seeds?
   (c) Actionability floor — named as a TEST ("one distinct
       marketing action per segment, tested by writing the action
       in one sentence per segment"), not a number.

3. SML path — draft the threshold-selection RULE (NOT the
   threshold value):
   (a) Curve to read — PR (for rare-positive churn and conversion),
       not ROC. Name the endpoint that produces the curve (per
       src/retail/backend/routes/predict.py).
   (b) Cost asymmetry — quote the $3 per-customer touch cost from
       PRODUCT_BRIEF.md §2 verbatim; the $120 CAC is in
       PLAYBOOK.md Phase 6 SML (not in the brief) — cite the
       Playbook line, not §2.
   (c) Calibration floor — Brier score cutoff; if breached, run
       isotonic calibration BEFORE threshold selection.

4. Compute the counterfactual dollar lift framework — NOT the
   number, the formula. "If K=N moves X customers off the
   $45/wrong-segment path, the monthly lift is $45 × X." I plug
   X when I see the leaderboard.

5. Timestamp the pre-registration — record the wall-clock time in
   the journal header. This is the only evidence that the floors
   preceded the results.

Do NOT propose floor values (0.25 silhouette, 0.80 Jaccard, 0.3
threshold). I write those values myself in the journal, at a
timestamp that precedes my next leaderboard read. If you propose a
value I use, my pre-registration is corrupted.

Any dollar figure you mention must be quoted from PRODUCT_BRIEF.md §2
(or PLAYBOOK.md Phase 6 SML for the $120 CAC). Do NOT invent.

Do NOT use "blocker" without a specific blocked action. An
un-set floor is not a blocker; it is the phase I am currently running.

When the journal has floor DEFINITIONS (USML) or the threshold-rule
FRAME (SML), a timestamp, and the lift-formula skeleton, stop and
wait for me to write the values.
```

### Why this prompt is written this way

- Inheritance-framed opening separates the SHAPE of commitment (three floors / PR+calibration, pre-committed by the scaffold and rubric) from the VALUES (mine to write) — this is the anti-post-hoc architecture of the phase.
- The "confirm you have not seen the winner" honesty clause is the pre-registration mechanic; without it, a silently-seen leaderboard leaks into the floor values.
- One paste serves both USML (3 floors) and SML (threshold rule + calibration) because Phase 6 is the single phase of the night where both tracks live — branching keeps students from running two different prompts and losing the pre-registration clock.
- Show-the-brief split — $3 from §2, $120 from `PLAYBOOK.md` Phase 6 SML — is called out because the rubric rewards correct citation and 0/4s a $120-from-§2 claim.
- Forbidding value proposals and requiring a timestamp is the D2 (metric→cost linkage) and D5 (reversal) guard together — floors without a timestamp score 0/4 on D2.

### What to expect back

- `journal/phase_6_usml.md` with separation / stability / actionability floor DEFINITIONS and a timestamp (USML), OR `journal/phase_6_sml.md` with the PR-curve + calibration rule and a timestamp (SML).
- An honest note of whether the leaderboard has been seen yet (ideally: "not yet").
- A lift-formula skeleton with brief-sourced unit costs and placeholder customer counts.
- Correct citation split: $3 → brief §2, $120 → `PLAYBOOK.md` Phase 6 SML.
- A stop signal pending my value-writing.

### Push back if you see

- A proposed floor value ("silhouette ≥ 0.25", "threshold 0.3") — "please remove the value; I write those myself. your job is the definition."
- No timestamp on the journal entry — "please add wall-clock time to the header so the order is auditable."
- $120 CAC cited to `PRODUCT_BRIEF.md §2` — "that's in `PLAYBOOK.md` Phase 6 SML, not the brief. please re-cite."
- ROC named as the SML threshold curve — "churn and conversion are rare-positive; please use PR, not ROC."
- Actionability floor expressed as a number (e.g. "0.6 on some actionability index") — "actionability is a test — 'one distinct action per segment', not a number."

### Adapt for your next domain

- Change `separation / stability / actionability` (USML) to your domain's three quality dimensions.
- Change `PR curve + Brier calibration` (SML) to the threshold-selection tool for your target (ROC if balanced; lift chart if ranking matters more than decisions).
- Change `$3 per touch / $120 CAC` cost asymmetry to your domain's FN / FP cost pair.
- Change `counterfactual vs 2020 rulebook` to counterfactual vs your incumbent baseline.
- Keep the timestamp + no-proposed-values mechanic as-is — it's domain-independent.

### Evaluation checklist

- [ ] Three floors declared AT VALUES (not "high silhouette").
- [ ] Floors committed BEFORE seeing the leaderboard (timestamp in journal).
- [ ] Dollar lift computed as counterfactual vs incumbent.
- [ ] Reversal condition named (specific signal + threshold + duration).
- [ ] Chosen K passes all three floors, not just the best one.

### Journal schema — universal

```
Phase 6 — Metric + Threshold
Primary metric: ____ (reason: ____)
Floor 1: ____ at ____ (committed at timestamp ____)
Floor 2: ____ at ____
Floor 3: ____ at ____  (USML only)
Chosen operating point: K = ____  /  threshold = ____
Counterfactual lift vs incumbent (in declared unit): ____
Reversal condition: signal ____ + threshold ____ + duration ____
```

> **Retail instantiation:** Separation floor = silhouette ≥ 0.25; Stability floor = bootstrap Jaccard ≥ 0.80; Actionability floor = one distinct campaign per segment. Chosen K = 5; lift = $14,800/month vs 2020 rulebook. Reversal: stability < 0.80 for 2 consecutive monthly re-clusters → drop to K=4.

### Common failure modes

- Floors set AFTER seeing the leaderboard — 0/4 on D2.
- Dollar lift stated as "higher is better" without counterfactual — 1/4 on D2.
- Reversal condition stated as "if data changes" — 0/4 on D5.
- "Actionability" floor skipped because it's not a number — scores 1/4 on D3; this is the single biggest Sprint 1 rubric trap.

### Artefact

`workspaces/.../journal/phase_6_usml.md` (and `phase_6_sml.md` when replayed in Sprint 2).

### Instructor pause point

- Sketch a silhouette curve that peaks at K=2 and drops off. Ask: why isn't K=2 the answer? (Because the actionability floor rejects it.)
- Ask every student to write separation and stability floors silently, then compare. Spread is usually 0.55–0.75 for separation, 0.70–0.85 for stability. Ask: how did you pick?
- Demonstrate: take two segments from K=7 that got nearly identical one-line actions. Collapse, keep, or defend the difference in dollars?

### Transfer to your next project

1. What are my three analogues of separation / stability / actionability — whatever "signal quality," "time-robustness," and "business-action-distinctness" mean in my domain?
2. Did I commit to numeric floors BEFORE seeing the leaderboard, and can I prove it (timestamps, journal order)?
3. Is my dollar-lift a counterfactual against the _current_ system being replaced, or a raw cost-of-error floating in a vacuum?

---

## Phase 6 (SML replay) — SML Metric + Threshold

### Concept

The SML variant that Week 4 couldn't go deep on. This is the classifier's threshold-selection phase. Read the PR curve, pick the operating point, tie it to dollars.

### Why it matters (SML lens — the DEPTH Week 4 skipped)

- **ROC curve** shows the classifier's ranking ability across all thresholds. AUC summarises it. **Use AUC when classes are balanced OR you care about ranking, not decisions.**
- **PR curve** shows precision vs recall across thresholds. **Use PR when positives are rare (churn, fraud, conversion) — ROC is overly optimistic on imbalanced data.**
- **Cost-based threshold selection.** For each threshold, compute expected cost = (P(FP) × cost_FP) + (P(FN) × cost_FN). Pick the threshold that minimises expected cost. This is what turns your leaderboard into a dollar decision.
- **Calibration** (Brier score, reliability diagram) — if the model says 30% probability, do 30% of those cases actually happen? A well-calibrated model's probabilities are trustworthy; a miscalibrated model's rankings are fine but its probabilities are not. If you use probabilities directly (e.g., expected-revenue allocator), calibration matters. Platt scaling and isotonic regression are the two standard fixes.
- **Class imbalance handling.** When positives are <10%: stratified sampling in CV, class weights in the loss, or SMOTE-style resampling. The threshold selection needs to happen AFTER rebalancing.

### Your levers this phase

- **Lever 1 (the big one): threshold on the PR curve.** For rare positives, find the threshold that maximises F1 or meets a precision target (e.g., "precision ≥ 0.6 at minimum recall 0.5").
- **Lever 2 (the cost-asymmetry):** if FN cost is 5× FP cost, push threshold LOWER (more alarms, catch more positives). If FP cost is 5× FN cost, push threshold HIGHER (fewer alarms, only confident positives).
- **Lever 3 (the calibration):** if you use the probability directly (not just rank), run calibration (Platt / isotonic). Raw GBM probabilities are usually miscalibrated.
- **Lever 4 (the imbalance):** stratified sampling, class weights, or resampling.

### Trust-plane question

At what threshold does this classifier earn its dollars?

### Paste this

> The paste-ready prompt for Phase 6 **covers both USML (Sprint 1 three-floor pre-registration) and SML (Sprint 2 PR-curve + Brier calibration)** via an explicit sprint branch at the top. See **§Phase 6 — Metric + Threshold** above. This SML-replay section retains its teaching content (PR vs ROC, cost-based threshold selection, calibration) as reference; the prompt itself is the same one you pasted when you reached Phase 6 in Sprint 2.

### Evaluation checklist

- [ ] PR curve read + operating point named (not "I chose 0.5 because default").
- [ ] Threshold tied to cost asymmetry (dollar math shown).
- [ ] Calibration checked (Brier); re-calibrated if needed.
- [ ] Class imbalance addressed (stratification / weights / resampling noted).
- [ ] Reversal condition named (what signal flips this threshold decision).

### Journal schema — universal

```
Phase 6 SML — Metric + Threshold
Primary metric: ____ (ROC-AUC / PR-AUC / F1 / precision@recall-X / calibrated-Brier)
Cost asymmetry: FN = $____, FP = $____, ratio = ____
Chosen threshold: ____ (expected cost = $____ per 1,000 predictions)
Calibration: Brier = ____ (adjusted? ____)
Class imbalance handling: ____
Reversal condition: signal ____ + threshold ____ + duration ____
```

> **Retail instantiation (churn):** CAC = $120, touch cost = $3 → ratio 40:1. Pick threshold at 0.22 (per PR curve); expected cost ≈ $1,800 per 1,000 predictions. Brier = 0.03 — no recalibration needed. Reversal: if 7-day calibration error > 0.05 for 2 weeks, re-train.

### Common failure modes

- Threshold at 0.5 because "that's the default" — 0/4 on D2.
- ROC used for rare-positive problem — threshold looks good but product is miscalibrated for imbalanced reality.
- Calibration skipped when probabilities feed downstream (allocator) — the downstream allocator optimizes against bad numbers.
- Reversal condition = "if model does poorly" — 0/4 on D5.

### Artefact

`POST /predict/threshold` with justification + `journal/phase_6_sml.md`.

### Instructor pause point

- Draw the PR curve on the whiteboard. Ask: why do we care about PR, not ROC, for churn?
- Ask: if touching everyone costs $3 and re-acquiring a churned customer costs $120, at what threshold do you send a retention offer? Compute live.
- Show a miscalibrated output (30% predicted → 50% actual). Ask: if the allocator uses this probability, what goes wrong?

### Transfer to your next project

1. Which curve applies to MY problem — ROC (balanced) or PR (rare positives)?
2. What is my cost asymmetry in dollars, and did my chosen threshold actually minimise expected cost (not just "feel right")?
3. Are my probabilities calibrated? If a downstream system uses them, calibration is not optional.

---

