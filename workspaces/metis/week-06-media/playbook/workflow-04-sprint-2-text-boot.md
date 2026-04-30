<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 4 — Sprint 2 Text Boot (Transformer text moderator)

> **What this step does:** Boot Sprint 2 by copying skeleton journal files for the Transformer replay, confirming the text-moderator endpoints, and getting a written orientation — before any Phase 4 SML prompt fires.
> **Why it exists:** Sprint 2 replays Phases 4–8 for the Transformer text moderator. Booting it cleanly means the SML phase pattern fires fast — without re-discovering scaffold details Sprint 1 already established.
> **You're here because:** Sprint 1 Vision wrapped (Phase 8 gate signed for the image moderator) and Sprint 2 is the Transformer replay.
> **Key concepts you'll see:** SML replay, fine-tuning vs prompting, calibration, cost-based threshold, three-family leaderboard

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Sprint 2 — the SML replay for the text moderator. Same five-
phase pattern as Sprint 1 (Phase 4 candidates → Phase 5 implications →
Phase 6 metric+threshold → Phase 7 red-team → Phase 8 deployment gate),
but applied to a different model class (transformer encoder).

Before I start the phase walk, I need you to:

1. Copy the SML replay skeletons from journal/skeletons/ into journal/.
   These have the _text suffix to distinguish them from the _vision pass.

2. Confirm the text-moderator endpoints are live by making GET requests.
   If any is not live, STOP and raise a hand.

3. Re-state — for THIS sprint's model class — the dollar asymmetry that
   drives Phase 6 thresholds. Quote the exact lines from the cost source.

4. Name the three-family leaderboard the scaffold ships. For each family,
   cite the file and function. Do NOT invent families that aren't in the
   scaffold.

5. Do NOT propose per-class thresholds. Those are my pre-registration in
   phase_6_text.md before I see the leaderboard.

6. Do NOT use the word "blocker" without naming a specific action.

Once skeletons are copied and endpoints confirmed live, summarise: the five
SML phases for this sprint, the per-class threshold shape (5 classes), the
calibration check (Brier + reliability diagram) that Phase 6 SML adds on
top of the threshold decision, and the Phase 7 sweeps specific to this
sprint's model class.

Then stop and wait for my Phase 4 prompt.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Sprint: Sprint 2 Text/Transformer — text moderator (5 classes: hate_speech,
harassment, threats, self_harm_encouragement, safe).

Phases covered: Playbook phases 4, 5, 6, 7, 8 (replay). Phases 1, 2, 3 were
framed in Sprint 1 — do NOT re-run them.

Skeleton copy: copy phase_{4..8}_text.md skeletons from journal/skeletons/
into workspaces/metis/week-06-media/journal/.

Endpoint checks (GET only):
- /moderate/text/leaderboard → 3-family × 5-class P/R/F1 + Brier
- /moderate/text/registry → registry state
If either is not live, STOP and raise a hand — do not debug.

Three-family leaderboard cite: the scaffold trains BERT-base + RoBERTa +
zero-shot LLM (the cheap-prompt baseline). Cite each in
src/media/backend/ml_context.py — e.g. "BERT-base, per train_baseline_text_bert
in src/media/backend/ml_context.py."

Dollar asymmetry restatement: $320 false-negative vs $15 false-positive =
21:1 ratio (PRODUCT_BRIEF.md §2). The text moderator's threshold for
self_harm_encouragement has clinical-safety floor considerations on top —
flag as "softer-than-CSAM but harder-than-cost-balanced" in the summary.
The IMDA $1M ceiling does NOT apply to text-only classes (CSAM-adjacent is
image-class only) — confirm this distinction.

Calibration: Phase 6 SML adds calibration on top of threshold. The scaffold
exposes /moderate/text/calibrate with platt and isotonic methods. Brier
score and reliability diagram both render in the viewer. Calibration matters
because the queue allocator (Sprint 3) consumes probabilities, not just
labels — miscalibrated probabilities corrupt the LP allocator's expected-
cost calculations.

Phase 7 sweeps to name (NOT execute): adversarial perturbation (typos,
unicode confusables, leetspeak), out-of-distribution language (Singlish vs
US English vs Malay code-mixing — the platform spans 5 SEA markets),
demographic-skew calibration check.

After the summary, stop and wait for my Phase 4 SML prompt.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Five skeleton files copied: `journal/phase_{4..8}_text.md` exist
- ✓ `/moderate/text/leaderboard` returned 3 families × 5 classes
- ✓ `/moderate/text/registry` returned registry state
- ✓ Summary names the five SML phases, the per-class threshold shape, and the calibration check
- ✓ Three Phase 7 sweeps named (adversarial / OOD / demographic-skew)
- ✓ Stop signal pending Phase 4 SML
- ✓ Viewer Sprint 2 tile activates

**Signals of drift — push back if you see:**

- ✗ A proposed threshold value (e.g. "hate-speech ≥ 0.80") — ask to remove
- ✗ A 4th model family invented (e.g. T5) — ask "which file in `src/media/backend/` defines this?"
- ✗ The IMDA $1M ceiling claimed for a text-only class — ask "isn't that the image CSAM-adjacent class?"
- ✗ Calibration described as optional — ask "the queue allocator consumes probabilities; isn't calibration load-bearing here?"

---

## 3. Things you might not understand in this step

- **SML replay** — Phases 4–8 run twice tonight, once per supervised modality (CNN in Sprint 1, Transformer in Sprint 2)
- **Fine-tuning vs prompting** — fine-tuning trains weights on your labels; prompting describes the task in a prompt and uses a frozen LLM. Different cost / consistency profiles
- **Calibration** — does "P=0.7" actually mean the model is right 70% of the time? Brier + reliability diagram answer this
- **Cost-based threshold** — the threshold that minimises expected cost on the holdout, given the FN/FP asymmetry
- **Three-family leaderboard** — BERT + RoBERTa + zero-shot LLM, all on the same labels for direct comparison

---

## 4. Quick reference (30 sec, generic)

### SML replay

Phases 4–8 are run twice tonight: once for the image moderator (Sprint 1 with CNN families), once for the text moderator (Sprint 2 with transformer families). Replay is a teaching tool — the same five-phase pattern fires on a different model class so the pattern itself becomes muscle memory. The journals carry suffixes (`_vision`, `_text`) so they don't overwrite each other. Skipping the replay is BLOCKED — the rubric counts both passes.

> **Deeper treatment:** [appendix/03-modeling/supervised-families.md](./appendix/03-modeling/supervised-families.md)

### Fine-tuning vs prompting

Fine-tuning trains a transformer's weights on your labelled data — expensive, consistent, domain-specific. Prompting describes the task in plain language to a frozen LLM (zero-shot or few-shot) — cheap, flexible, less reliable on subtle cases. Tonight's three-family leaderboard pits BERT-base fine-tune + RoBERTa fine-tune against a zero-shot LLM baseline. The decision in Phase 5 SML is which family wins on YOUR cost asymmetry (21:1 favouring recall on harmful) — not which is "best in general."

> **Deeper treatment:** [appendix/03-modeling/supervised-families.md](./appendix/03-modeling/supervised-families.md)

### Calibration

A model's P=0.7 is calibrated if, across many P=0.7 predictions, the model is right 70% of the time. Brier score measures squared error vs the true label; reliability diagrams plot predicted vs observed frequency. Calibration matters tonight because the queue allocator (Sprint 3) consumes probabilities directly. A miscalibrated text moderator scoring P=0.95 when the truth is P=0.6 corrupts the LP allocator's expected-cost calculation, which corrupts the queue plan, which corrupts SLA.

> **Deeper treatment:** [appendix/04-evaluation/calibration-and-brier.md](./appendix/04-evaluation/calibration-and-brier.md)

### Cost-based threshold

The threshold per class that minimises (FN cost × FN rate + FP cost × FP rate) on the holdout, given the 21:1 asymmetry. For text moderation tonight: a hate-speech threshold of 0.85 might give 92% precision + 78% recall (high-precision, lower-recall — favours not removing legitimate content). A threshold of 0.70 might give 84% precision + 89% recall (lower-precision, higher-recall — favours catching harm). Which wins depends on $320 × FN rate vs $15 × FP rate at each threshold.

> **Deeper treatment:** [appendix/04-evaluation/pr-curve.md](./appendix/04-evaluation/pr-curve.md)

### Three-family leaderboard

BERT-base fine-tune + RoBERTa fine-tune + zero-shot LLM (e.g. Claude or GPT-4 with a moderation-instruction prompt) all evaluated on the same 5 classes on the same holdout. The leaderboard shows P/R/F1 + Brier per family per class. The decision in Phase 5 is which family to ship — and the decision is rarely "the highest F1." A higher-F1 family that's miscalibrated may lose to a lower-F1 family with better reliability for downstream consumption.

> **Deeper treatment:** [appendix/03-modeling/supervised-families.md](./appendix/03-modeling/supervised-families.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Sprint 2 (text
moderator), where I am building an ML system for MosaicHub.

Read `workspaces/metis/week-06-media/playbook/workflow-04-sprint-2-text-boot.md`
for what this step does, and read `workspaces/metis/week-06-media/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. calibration >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current MosaicHub state
3. Implications for the decision I'm about to make (or just made) in Sprint 2
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

- [ ] Five skeleton files exist (`journal/phase_{4..8}_text.md`)
- [ ] `/moderate/text/leaderboard` returned 3 families × 5 classes
- [ ] `/moderate/text/registry` returned registry state
- [ ] Summary written: 5 SML phases, per-class threshold shape, calibration check, 3 Phase 7 sweeps
- [ ] Claude Code stopped, waiting for Phase 4 SML prompt

**Next file:** [`phase-04-candidates.md`](./phase-04-candidates.md) (SML pass)
