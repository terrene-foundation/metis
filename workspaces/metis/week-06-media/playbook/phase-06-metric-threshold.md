<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 6 — Metric + Threshold (per-class × 5)

> **What this phase does:** For each of the 5 classes in the chosen moderator, set the auto-remove threshold — defended in $ of (FN cost × FN rate + FP cost × FP rate) at that operating point. csam_adjacent is hard-floor (IMDA), not cost-balanced.
> **Why it exists:** This IS the moderation product. The threshold per class is the auto-decision rule the platform ships. Get it wrong and either harm escapes (FN, $320 each) or creators get unfairly auto-removed (FP, $15 each).
> **You're here because:** Phase 5 picked the model. Phase 6 turns it into auto-decisions.
> **Key concepts you'll see:** PR curve per class, cost-balanced threshold, IMDA hard floor, calibration check, pre-registered floors

---

## 1. Paste this into Claude Code

**Universal core:**

```
I'm in Playbook Phase 6 — Metric + Threshold. For each of the 5 classes
in the moderator, propose a threshold. For each:

1. Show the PR curve at K threshold candidates (e.g. 0.5 / 0.6 / 0.7 /
   0.8 / 0.9 / 0.95). For each candidate compute (FN cost × FN rate
   + FP cost × FP rate) on the holdout.
2. Identify the cost-minimum threshold for the class.
3. Note the calibration check (Brier-pass / Brier-fail).
4. State which class needs a HARD-FLOOR threshold (regulator-mandated)
   and what the regulator's floor is.

Do NOT propose the FINAL threshold value — I pre-registered the floor
shape (e.g. "max-cost-acceptable" or "min-recall-floor") in Phase 5.
You produce the curve and the cost-minimum; I write the final value
into the journal.

Do NOT use "blocker" without specifics.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Sprint detection:
- Sprint 1 (Vision): 5 image classes (nsfw, violence, weapons,
  csam_adjacent, safe). 5 thresholds.
- Sprint 2 (Text): 5 text classes (hate_speech, harassment, threats,
  self_harm_encouragement, safe). 5 thresholds.

Cost asymmetry: $320 FN / $15 FP = 21:1. Cite PRODUCT_BRIEF.md §2.

CRITICAL — IMDA hard floor on csam_adjacent (Sprint 1 only):
- The IMDA mandate says any post scoring >0.4 on csam_adjacent must
  be routed to mandatory human review within 60 seconds. The hard
  floor is therefore 0.4 (NOT cost-balanced — regulator-mandated).
- Phase 6 treats csam_adjacent SEPARATELY: produce the PR curve, but
  the auto-remove threshold MUST be at most 0.4 (not above) for the
  hard-floor compliance. The cost-balanced minimum may be higher
  (e.g. 0.85), but the regulator wins.
- BEFORE the IMDA injection fires (Sprint 3): csam_adjacent threshold
  is cost-balanced. AFTER the injection: hard-floor 0.4. Sprint 1's
  Phase 6 sets the cost-balanced version; Sprint 3's Phase 11 re-run
  shifts it to hard-floor.

self_harm_encouragement (Sprint 2 only):
- Clinical-safety floor: any predicted score above 0.5 should at
  minimum surface a content-warning + helpline link AND queue for
  human review. Cost-balanced math may set auto-remove higher
  (e.g. 0.85), but the warn-and-queue is non-negotiable.
- Surface this dual-action explicitly in the journal.

Calibration:
- Phase 5 ensured Brier ≤ pre-registered floor. If a class's Brier
  on the chosen model exceeds the floor, flag it AS A FINDING (not
  blocker, finding) and note that Phase 13 must monitor calibration
  decay tightly for that class.

Endpoint to call:
- Sprint 1: POST /moderate/image/threshold per class with action
  (auto_remove / human_review / allow)
- Sprint 2: POST /moderate/text/threshold per class with action

Journal file: copy journal/skeletons/phase_6_metric_threshold.md
(suffix _vision in Sprint 1, _text in Sprint 2).
```

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ 5 PR curves drawn (one per class)
- ✓ Cost-balanced threshold computed per class with the math shown
- ✓ csam_adjacent (Sprint 1): hard-floor at 0.4 noted SEPARATELY from cost-balanced
- ✓ self_harm_encouragement (Sprint 2): warn-and-queue dual action surfaced
- ✓ Calibration findings flagged
- ✓ POST to /moderate/{image,text}/threshold per class made
- ✓ Stop signal pending Phase 7

**Signals of drift — push back if you see:**

- ✗ A single threshold proposed across all classes — ask "we have 5 classes; one threshold can't be right"
- ✗ csam_adjacent treated as cost-balanced — ask "isn't the IMDA $1M ceiling structural? this should be hard-floor"
- ✗ self_harm_encouragement set without warn-and-queue — ask "clinical-safety dual-action?"
- ✗ Cost math without quoted brief lines — ask for citations
- ✗ Phase 7 not flagged for low-Brier classes

---

## 3. Things you might not understand in this phase

- **PR curve per class** — precision vs recall as threshold sweeps
- **Cost-balanced threshold** — the threshold that minimises expected $ on the holdout
- **IMDA hard floor** — regulator-mandated minimum, structural over cost-balanced
- **Calibration check** — Brier confirms the model's probabilities are honest
- **Pre-registered floors** — the threshold shape you committed to BEFORE seeing leaderboard results

---

## 4. Quick reference (30 sec, generic)

### PR curve per class

For each class, plot precision vs recall as the threshold sweeps from 0 to 1. The curve shows the trade-off: higher threshold = higher precision but lower recall. The cost-balanced minimum is the operating point that minimises (FN cost × FN rate + FP cost × FP rate). Different classes have different optimum thresholds — there is no universal "0.5".

> **Deeper treatment:** [appendix/04-evaluation/pr-curve.md](./appendix/04-evaluation/pr-curve.md)

### Cost-balanced threshold

The threshold that minimises expected $ on the holdout, given the FN/FP cost asymmetry. For 21:1 (tonight), the cost-balanced threshold sits LOWER than the F1-maximising threshold — you're willing to accept more FP to catch more FN because each FN costs 21× as much. The math: scan thresholds, compute FN_count × $320 + FP_count × $15 at each, pick the minimum.

> **Deeper treatment:** [appendix/04-evaluation/pr-curve.md](./appendix/04-evaluation/pr-curve.md)

### IMDA hard floor

A regulator-mandated maximum allowed score before mandatory routing. csam_adjacent: any post above 0.4 must be human-reviewed within 60 seconds. This is structural over cost-balanced — even if the cost minimum is 0.85, the auto-remove threshold cannot exceed 0.4 because the regulator owns the rule. The hard floor is the kind of constraint Phase 11 classifies as "hard, not soft."

> **Deeper treatment:** [appendix/07-governance/hard-vs-soft-constraints.md](./appendix/07-governance/hard-vs-soft-constraints.md)

### Calibration check

Brier score: average squared error between predicted P and observed outcome. Brier ≤ 0.10 = well-calibrated. Brier > 0.20 = miscalibrated. Tonight's queue allocator consumes probabilities, so calibration matters. A class with high Brier needs Phase 13 to monitor calibration decay tightly.

> **Deeper treatment:** [appendix/04-evaluation/calibration-and-brier.md](./appendix/04-evaluation/calibration-and-brier.md)

### Pre-registered floors

The threshold SHAPE committed to before seeing the leaderboard — e.g. "I will accept a threshold that gets at least 0.80 recall on csam_adjacent" or "I will reject any threshold whose FP rate exceeds 5%." Pre-registration prevents post-hoc rationalisation: if you saw the leaderboard and then wrote "0.80 recall is acceptable", the floor is meaningless.

> **Deeper treatment:** [appendix/04-evaluation/pre-registered-floors.md](./appendix/04-evaluation/pre-registered-floors.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Phase 6.

Read the phase file and `workspaces/metis/week-06-media/journal/phase_6_metric_threshold*.md`.

Explain "<<< FILL IN: concept name >>>" — plain language, MosaicHub-grounded,
implications for Phase 6 thresholds, what to push back on. Under 400 words.
```

---

## 6. Gate / next

- [ ] 5 PR curves drawn, cost-balanced threshold per class computed
- [ ] csam_adjacent hard-floor noted separately (Sprint 1)
- [ ] self_harm_encouragement warn-and-queue surfaced (Sprint 2)
- [ ] Calibration findings flagged
- [ ] POST per class to threshold endpoint
- [ ] Stop signal pending Phase 7

**Next file:** [`phase-07-redteam.md`](./phase-07-redteam.md)
