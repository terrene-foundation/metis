<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 6 — Sprint 4 MLOps Boot (drift × 3 cadences)

> **What this step does:** Boot Sprint 4 by copying the Phase 13 skeleton, confirming drift endpoints are live for all three model IDs, and orienting on why the three retrain rules sit at three different cadences.
> **Why it exists:** Most students try to write one universal retrain rule that fires across all three models. That fails the rubric. Booting cleanly forces you to confront the three-cadence reality before you write the rule.
> **You're here because:** Sprint 3 wrapped (Phase 12 post-IMDA accepted) and Sprint 4 closes the chain.
> **Key concepts you'll see:** drift × 3 cadences, PSI, calibration decay, seasonal exclusion, HITL on first trigger

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Sprint 4 — MLOps drift monitoring. Three drift rules, three
cadences, three signals. Phase 13 fires once but covers all three models.

Before I start Phase 13, I need you to:

1. Copy the Phase 13 skeleton from journal/skeletons/phase_13_retrain.md
   into journal/.

2. Confirm /drift/status/{model_id} returns reference_set: true for all
   three IDs (image_moderator, text_moderator, fusion_moderator).

3. State, in writing: why the three models drift at three different
   cadences and what signals are appropriate for each. Do NOT propose
   threshold values; those are my pre-registration call in
   phase_13_retrain.md.

4. Name the seasonal exclusions explicitly. Election cycles and major
   news events spike adversarial content; auto-retraining on those windows
   bakes the spike into the model. Cite from PRODUCT_BRIEF.md.

5. Do NOT use the word "blocker" without naming a specific action.

Once skeleton is copied and endpoints confirmed live, summarise: the three
cadences (image weekly / text daily / fusion per-incident), the signal per
cadence, the role of HITL on first trigger, and the seasonal exclusions.

Then stop and wait for my Phase 13 prompt.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Sprint: Sprint 4 MLOps — drift × 3 models.
Phase: Playbook phase 13 (one entry covers all three models).

Skeleton copy: copy phase_13_retrain.md from journal/skeletons/ into journal/.

Endpoint checks (GET only):
- /drift/status/image_moderator → reference_set: true
- /drift/status/text_moderator → reference_set: true
- /drift/status/fusion_moderator → reference_set: true
If any returns reference_set: false, STOP and raise a hand — do not re-seed.

Why three cadences (NAME, do NOT pick threshold values):
- IMAGE moderator: visual style moves slowly; per-class score distribution
  + per-pixel-domain distribution; cadence WEEKLY. Spike-on-spike is rare.
- TEXT moderator: language moves fast; token frequency + embedding
  distribution + per-class calibration; cadence DAILY. Slang, dogwhistles,
  evolving codewords drift in days.
- FUSION moderator: adversaries probe joint seams in real time; cross-modal
  alignment-score variance + per-incident calibration decay; cadence
  PER-INCIDENT (any complaint that touches a high-fusion-confidence post
  triggers a check).

Signals per cadence (NAME, do NOT propose thresholds):
- IMAGE: PSI per per-class score distribution; image-domain PSI on a
  representative pixel-feature embedding.
- TEXT: token-frequency PSI on top-1000 tokens; calibration decay (Brier
  delta vs registered baseline); per-class score-distribution PSI.
- FUSION: cross-modal alignment-score variance vs registered baseline;
  per-incident calibration check on the post that triggered the complaint.

Seasonal exclusions (cite from PRODUCT_BRIEF.md): Nov–Dec? No — that's
Week 5. Tonight: election cycles + major news events (PRODUCT_BRIEF.md §2,
"Peak season"). Auto-retraining during these windows bakes the adversarial
spike into the model and lowers the moderator's recall on harm permanently.

HITL on first trigger: every retrain rule fires HITL on first trigger.
After the first trigger AND a successful re-train AND a 30-day stable
window, the rule may auto-fire on subsequent triggers (per
appendix/07-governance/hitl-patterns.md).

After the summary, stop and wait for my Phase 13 prompt.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Skeleton copied: `journal/phase_13_retrain.md`
- ✓ All three `/drift/status/{model_id}` endpoints returned `reference_set: true`
- ✓ Summary names the three cadences (weekly / daily / per-incident) with rationale per cadence
- ✓ Summary names the signals per cadence (PSI variants, calibration decay, alignment-score variance)
- ✓ Seasonal exclusions cited from `PRODUCT_BRIEF.md §2`
- ✓ HITL-on-first-trigger named
- ✓ Stop signal pending Phase 13
- ✓ Viewer Sprint 4 tile activates

**Signals of drift — push back if you see:**

- ✗ A single universal cadence proposed (e.g. "weekly across all three") — ask "what's the rationale per model? language drifts faster than visual style."
- ✗ Threshold values proposed (e.g. "PSI > 0.25") — ask to remove
- ✗ "Auto-retrain immediately on trigger" — ask "where's HITL on first trigger? PRODUCT_BRIEF says first-trigger is HITL."
- ✗ Seasonal exclusions described as Nov–Dec (that's Week 5) — ask "isn't tonight's seasonal exclusion election cycles + major news events?"
- ✗ A `reference_set: false` ignored — ask "the reference is missing for this model; isn't that a scaffold bug?"

---

## 3. Things you might not understand in this step

- **Drift cadence stratification** — different models drift at different speeds; one universal retrain rule fails
- **PSI (Population Stability Index)** — measures how much a distribution has shifted from a registered baseline
- **Calibration decay** — even if accuracy holds, the probabilities can become miscalibrated as the world drifts
- **HITL on first trigger** — first time a retrain rule fires, a human approves before retraining auto-runs
- **Seasonal exclusion** — windows of expected adversarial spike; auto-retraining on these bakes the spike in

---

## 4. Quick reference (30 sec, generic)

### Drift cadence stratification

The three models drift at three speeds. Visual style is slow — fashion changes weekly, not daily. Language is fast — slang and dogwhistles change daily. Adversarial joint-modal attacks are real-time — adversaries probe seams as soon as they discover them. A universal retrain rule (e.g. "weekly across all three") under-reacts on text and over-reacts on image. Phase 13 demands three rules, each with a cadence grounded in the modality's drift speed.

> **Deeper treatment:** [appendix/06-monitoring/drift-types.md](./appendix/06-monitoring/drift-types.md)

### PSI (Population Stability Index)

A simple statistic that measures how much a distribution has shifted: sum over bins of `(p_now - p_ref) * ln(p_now / p_ref)`. PSI < 0.1 = no meaningful shift; PSI 0.1–0.25 = moderate; PSI > 0.25 = significant. Used tonight for per-class score distributions (image), token frequencies (text), and alignment-score distributions (fusion). The thresholds you set in Phase 13 are PSI-floor values per signal.

> **Deeper treatment:** [appendix/06-monitoring/psi.md](./appendix/06-monitoring/psi.md)

### Calibration decay

Brier score or reliability-diagram drift over time. Even if F1 holds, the model's P=0.7 may now correspond to actual frequency P=0.55 — the labels still come out right but the probabilities lie. Calibration decay matters tonight because the queue allocator (Sprint 3) consumes probabilities, not labels. A miscalibrated text moderator silently corrupts the LP allocator's expected-cost calculation.

> **Deeper treatment:** [appendix/06-monitoring/calibration-decay.md](./appendix/06-monitoring/calibration-decay.md)

### HITL on first trigger

The first time a retrain rule fires (signal exceeds threshold over the duration window), a human reviewer approves before the retrain auto-runs. After the first successful retrain AND a 30-day stable window, the rule may auto-fire on subsequent triggers. The first-trigger HITL exists because false-positive triggers (one bad data day) can cause catastrophic auto-retrains that destabilise the model. After the rule has proven itself over 30 days, the human becomes optional.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

### Seasonal exclusion

A window of expected adversarial spike (election cycles, major news events) during which auto-retraining is suspended. The reason: an auto-retrain on a spike bakes the adversarial pattern into the model — the moderator learns to over-flag election speech, then the spike ends and the moderator over-flags ordinary political speech for the next quarter. Seasonal exclusion is a hard constraint on retrain-rule firing.

> **Deeper treatment:** [appendix/06-monitoring/retrain-rules.md](./appendix/06-monitoring/retrain-rules.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Sprint 4 (drift),
where I am building an ML system for MosaicHub.

Read `workspaces/metis/week-06-media/playbook/workflow-06-sprint-4-mlops-boot.md`
for what this step does, and read `workspaces/metis/week-06-media/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. drift cadence stratification >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current MosaicHub state
3. Implications for the decision I'm about to make (or just made) in Sprint 4
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

- [ ] Skeleton copied (`phase_13_retrain.md`)
- [ ] All three `/drift/status/{model_id}` returned `reference_set: true`
- [ ] Summary names three cadences with rationale, three signals, seasonal exclusions, HITL-on-first-trigger
- [ ] Claude Code stopped, waiting for Phase 13 prompt

**Next file:** [`phase-13-drift.md`](./phase-13-drift.md)
