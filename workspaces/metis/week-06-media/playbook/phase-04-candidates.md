<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 4 — Candidates (Vision in Sprint 1, Text in Sprint 2)

> **What this phase does:** Sweep a small candidate space to produce a leaderboard the next phase will read. Sprint 1 sweeps unfreeze-depth on the CNN backbone. Sprint 2 sweeps three transformer families.
> **Why it exists:** No single architecture is best for moderation a priori. Phase 5 picks the winner; Phase 4 produces the leaderboard the pick is grounded in.
> **You're here because:** Phase 3 closed feature decisions. Phase 4 is the candidate sweep.
> **Key concepts you'll see:** unfreeze-depth sweep (Sprint 1), three-family leaderboard (Sprint 2), per-class P/R/F1, holdout protocol, baseline-to-beat

---

## 1. Paste this into Claude Code

**Universal core:**

```
I'm in Playbook Phase 4 — Candidates. The scaffold ships ONE pre-trained
baseline; my job here is to sweep variations on the baseline (NOT new
architectures) so Phase 5 has a leaderboard to read.

Run the sweep. For each candidate, log:
- Per-class P/R/F1 on the holdout
- Brier score per class (calibration)
- Wall-clock training time
- Wall-clock inference time per sample (for Phase 10 cost reasoning)

Compare against the baseline in the leaderboard.

Do NOT propose which candidate wins — that's Phase 5.
Do NOT introduce architectures not in scope (no AutoML, no random search).
Do NOT use "blocker" without specifics.

When the leaderboard is written, stop.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Sprint detection: which sprint am I in?
- Sprint 1 (Vision): sweep unfreeze depth on the ResNet-50 backbone.
  Candidates: frozen / partial-unfreeze (last 2 conv blocks) / full-unfreeze.
  Endpoint: POST /moderate/image/finetune with unfreeze_layers ∈ {0, 2, all}.
- Sprint 2 (Text): sweep three transformer families.
  Candidates: bert_base / roberta / zero_shot_llm.
  Endpoint: POST /moderate/text/finetune with family ∈ {bert_base, roberta,
  zero_shot_llm}. (zero_shot_llm "fine-tune" is a no-op — it just produces
  the zero-shot leaderboard entry.)

Configuration:
- 3 trials per candidate, seed in {RANDOM_SEED, RANDOM_SEED+1, RANDOM_SEED+2}
- 2 epochs Sprint 1 / 3 epochs Sprint 2 (constrained by 50-min budget)
- Holdout: 10% of labelled posts (post-balanced for class imbalance)

Baseline-to-beat:
- Existing rule-keyword system: 31% recall on harmful, 4% FP rate.
  Cite from PRODUCT_BRIEF.md §1. Any candidate not beating this on
  harmful-class recall is BLOCKED from Phase 5 promotion.

Endpoint to call:
- Sprint 1: POST /moderate/image/finetune with each unfreeze setting
- Sprint 2: POST /moderate/text/finetune with each family

Result file: data/leaderboard.json (overwritten per sprint, with
sprint_tag in the JSON to distinguish vision vs text leaderboards).

Journal file: copy journal/skeletons/phase_4_candidates.md (apply
_vision suffix in Sprint 1, _text suffix in Sprint 2).
```

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Leaderboard written with 3 candidates × 3 seeds = 9 rows
- ✓ Per-class P/R/F1 + Brier per row
- ✓ Wall-clock training time + inference time per sample
- ✓ Comparison to 31% recall / 4% FP baseline cited
- ✓ No "winner" proposed (Phase 5 owns)
- ✓ Stop signal pending Phase 5

**Signals of drift — push back if you see:**

- ✗ A "winner" announced — ask to remove (Phase 5 owns)
- ✗ Architectures outside the 3-candidate space — ask "what's the source for this?"
- ✗ Missing per-class metrics (only overall accuracy reported) — ask for per-class
- ✗ Brier score missing — ask "we need calibration for the queue allocator"
- ✗ Wall-clock missing — ask "Phase 10 needs this for cost reasoning"

---

## 3. Things you might not understand in this phase

- **Unfreeze depth (Sprint 1)** — how much of the CNN backbone is fine-tuned vs frozen
- **Three-family leaderboard (Sprint 2)** — BERT vs RoBERTa vs zero-shot LLM
- **Per-class P/R/F1** — the moderator has 5 classes; aggregate metrics hide per-class failure
- **Holdout protocol** — how the held-out test set is constructed
- **Baseline-to-beat** — the rule-keyword system the new model must outperform on harm-recall

---

## 4. Quick reference (30 sec, generic)

### Unfreeze depth (Sprint 1)

How much of the pre-trained CNN backbone has its weights unfrozen during fine-tuning. Frozen (0 layers) = only the 5-class head trains; cheap, robust, may underfit. Partial-unfreeze (last 2 conv blocks) = some adaptation to moderation domain; balanced. Full-unfreeze (entire backbone) = max adaptation; expensive, can overfit on 80k samples. The sweep produces the trade-off curve Phase 5 reads.

> **Deeper treatment:** [appendix/03-modeling/supervised-families.md](./appendix/03-modeling/supervised-families.md)

### Three-family leaderboard (Sprint 2)

BERT-base fine-tuned + RoBERTa fine-tuned + zero-shot LLM (Claude or GPT-4 with a moderation prompt). Each scored on the same 5 classes on the same holdout. The zero-shot LLM is the "cheap baseline" — pay-per-call but no training time. Phase 5 picks among these based on (cost asymmetry × per-class P/R) + calibration + inference cost.

> **Deeper treatment:** [appendix/03-modeling/supervised-families.md](./appendix/03-modeling/supervised-families.md)

### Per-class P/R/F1

For a 5-class moderator, aggregate accuracy hides per-class failure. A model with 95% overall accuracy could have 60% recall on weapons (catastrophic) and 99% recall on safe (irrelevant). Per-class P/R/F1 surfaces the per-class story. The IMDA-bound CSAM-adjacent class needs separate scrutiny.

> **Deeper treatment:** [appendix/04-evaluation/pr-curve.md](./appendix/04-evaluation/pr-curve.md)

### Holdout protocol

How the held-out test set is constructed. Tonight: 10% stratified by class to handle imbalance, time-respected (held-out posts are LATER than training posts to avoid temporal leakage), demographic-balanced (proportional across the 5 SEA markets). The protocol matters — a non-stratified holdout under-represents the rare classes the model most needs to get right.

> **Deeper treatment:** [appendix/02-data/data-audit.md](./appendix/02-data/data-audit.md)

### Baseline-to-beat

The existing rule-keyword system: 31% recall on harm, 4% FP rate. Any candidate that fails to clear this baseline on harm-recall is BLOCKED from Phase 5 promotion. This is the structural floor that prevents shipping a fancy model that's worse than the rules. Cite the baseline numbers from `PRODUCT_BRIEF.md §1`.

> **Deeper treatment:** [appendix/03-modeling/naive-baselines.md](./appendix/03-modeling/naive-baselines.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Phase 4.

Read the phase file and `workspaces/metis/week-06-media/journal/phase_4_candidates*.md`
(_vision in Sprint 1, _text in Sprint 2).

Explain "<<< FILL IN: concept name >>>" — plain language, MosaicHub-grounded,
implications for my Phase 4 sweep, what to push back on. Under 400 words.
```

---

## 6. Gate / next

- [ ] Leaderboard has 3 candidates × 3 seeds with full per-class metrics
- [ ] Brier and wall-clock recorded
- [ ] Comparison to 31%/4% baseline cited
- [ ] No winner announced
- [ ] Stop signal pending Phase 5

**Next file:** [`phase-05-implications.md`](./phase-05-implications.md)
