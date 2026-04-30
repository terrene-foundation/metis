<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 5 — Implications (pick the candidate)

> **What this phase does:** Read the Phase 4 leaderboard and pick the candidate to ship — defended in $ of cost-asymmetry × per-class metrics + calibration + inference cost. Sprint 3 multi-modal pass picks fusion architecture.
> **Why it exists:** A leaderboard alone isn't a decision. Phase 5 is the load-bearing pick. Without it, Phase 6 has no model to threshold.
> **You're here because:** Phase 4 produced a leaderboard. Phase 5 picks.
> **Key concepts you'll see:** cost-asymmetry-weighted decision, calibration as tiebreaker, inference-cost ceiling, multi-modal architecture pick, ensemble-is-king-but

---

## 1. Paste this into Claude Code

**Universal core:**

```
I'm in Playbook Phase 5 — Implications. Read data/leaderboard.json (the
relevant sprint's leaderboard). For each candidate compute:

1. Cost-asymmetry-weighted score: ($FN cost × per-class FN rate) +
   ($FP cost × per-class FP rate), summed across classes
2. Calibration: Brier score per class
3. Inference-cost: $ per 1k inferences using the daily volume

Recommend ONE candidate. Defend in 1–2 paragraphs:
- What you sacrificed by NOT picking each other candidate
- Why this candidate's calibration is acceptable for the downstream
  consumer (queue allocator in Sprint 3)
- Why inference cost is feasible at the daily volume

Do NOT promote without me approving the recommendation.
Do NOT use "blocker" without specifics.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Sprint detection:
- Sprint 1 (Vision): pick unfreeze depth (frozen / partial / full)
- Sprint 2 (Text): pick family (bert_base / roberta / zero_shot_llm)
- Sprint 3 (Multi-modal): pick fusion architecture (early / late / joint)

For Sprints 1 + 2:
- Cost asymmetry: $320 FN / $15 FP (ratio 21:1) — cite PRODUCT_BRIEF.md §2
- IMDA $1M ceiling on csam_adjacent: hard floor, not cost-balanced.
  Phase 5 must defend csam_adjacent SEPARATELY from cost-balanced math.
- Daily volume: 600,000 image classifications / day (Sprint 1) or
  2,000,000 text classifications / day (Sprint 2)
- GPU inference cost: $0.03 per 1,000 image classifications (cite PRODUCT_BRIEF.md §2)
- Inference-cost feasibility: candidate × daily volume × $/1k must fit in
  the team's compute budget (state assumed budget if not in brief)

For Sprint 3 (Multi-modal):
- Fusion architecture trade-off:
  * early-fusion: cheap, brittle on adversarial
  * late-fusion: modular, slower retrain
  * joint-embedding: ~3× compute, best on cross-modal harm
- Multi-modal coverage gain vs compute-cost delta:
  estimate cross-modal-harm catches per day × $320 FN avoided vs
  ($0.03/1k × 600k images × 3× compute multiplier) = $/day cost
- The pick must be defensible as "joint pays for itself" or "late-fusion
  is enough" or "early-fusion is the right starting point because we
  can iterate weekly".

Journal file: copy journal/skeletons/phase_5_implications.md (suffix by
sprint: _vision / _text / _fusion).
```

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Cost-asymmetry-weighted score computed per candidate
- ✓ Calibration (Brier) per class per candidate
- ✓ Inference cost in $/day computed at the daily volume
- ✓ Recommendation made WITH explicit sacrifices for unpicked candidates
- ✓ csam_adjacent defended separately from cost-balanced math
- ✓ Sprint 3: fusion architecture compute-cost delta computed
- ✓ Stop signal pending review

**Signals of drift — push back if you see:**

- ✗ Recommendation without sacrifice statement — ask "what did the unpicked candidates lose by?"
- ✗ csam_adjacent folded into cost-balanced score — ask "isn't that hard-floor structurally?"
- ✗ Inference cost missing — ask "what's $/day at our volume?"
- ✗ Sprint 3: "joint-embedding obviously best" — ask "what's the daily $ cost?"
- ✗ Auto-promote without my approval — ask to wait

---

## 3. Things you might not understand in this phase

- **Cost-asymmetry-weighted decision** — the 21:1 FN/FP imbalance turns the leaderboard into a $ ranking
- **Calibration as tiebreaker** — when two candidates tie on F1, calibration breaks the tie
- **Inference-cost ceiling** — $/day at the daily volume must fit in compute budget
- **Multi-modal architecture pick (Sprint 3)** — early / late / joint, defended in coverage × $
- **Ensemble-is-king-but** — ensembles often win on F1 but lose on calibration + cost; not always best

---

## 4. Quick reference (30 sec, generic)

### Cost-asymmetry-weighted decision

The 21:1 FN/FP ratio means "candidate A scores 0.85 F1 / 0.92 recall" and "candidate B scores 0.87 F1 / 0.84 recall" can flip in $ ranking. Compute (FN cost × FN count + FP cost × FP count) at each candidate's operating point. The lower-$ candidate wins, regardless of F1. The IMDA $1M ceiling sits SEPARATELY — it forces csam_adjacent to a regulator-mandated minimum threshold, not a cost-balanced one.

> **Deeper treatment:** [appendix/04-evaluation/pr-curve.md](./appendix/04-evaluation/pr-curve.md)

### Calibration as tiebreaker

When two candidates have similar F1 / cost-asymmetry score, calibration (Brier) breaks the tie. Calibration matters because Sprint 3's queue allocator consumes probabilities directly. A miscalibrated model with P=0.95 when actual is P=0.60 corrupts the LP allocator's expected-cost calculation. Lower Brier = better calibration = better LP input.

> **Deeper treatment:** [appendix/04-evaluation/calibration-and-brier.md](./appendix/04-evaluation/calibration-and-brier.md)

### Inference-cost ceiling

$/day at the daily volume. 600k images × $0.03/1k = $18/day for image inference at the baseline. A fusion model at 3× compute = $54/day. A team budget of $100/day on inference imposes a hard ceiling. Phase 5's pick must fit under it; Phase 8 gate validates this before promote-to-shadow.

> **Deeper treatment:** [appendix/03-modeling/supervised-families.md](./appendix/03-modeling/supervised-families.md)

### Multi-modal architecture pick

Sprint 3 picks fusion arch on coverage × $ trade-off. Joint-embedding catches ~5% more cross-modal harm than late-fusion at our scale. 5% of 100k cross-modal posts/day = 5,000 catches × $320 FN saved = $1,600,000/year value. Compute cost delta: $54-$18 = $36/day = $13,140/year. Joint pays for itself ~120:1 — IF coverage gain is real (Phase 7 confirms). Without Phase 7 confirmation, the gain is theoretical.

> **Deeper treatment:** [appendix/03-modeling/recommender-families.md](./appendix/03-modeling/recommender-families.md)

### Ensemble-is-king-but

For tabular SML, gradient-boosted ensembles usually win F1 — and tonight's text moderator is one such case. But ensembles often have worse calibration than single models, and the queue allocator consumes probabilities. A GBM that wins on AUC but is miscalibrated produces worse plans than a single BERT with isotonic post-calibration. "Ensemble is king" is heuristic, not law.

> **Deeper treatment:** [appendix/03-modeling/supervised-families.md](./appendix/03-modeling/supervised-families.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Phase 5.

Read the phase file and `workspaces/metis/week-06-media/journal/phase_5_implications*.md`.

Explain "<<< FILL IN: concept name >>>" — plain language, MosaicHub-grounded,
implications for Phase 5 pick, what to push back on. Under 400 words.
```

---

## 6. Gate / next

- [ ] Cost-asymmetry-weighted score per candidate computed
- [ ] Calibration (Brier) per class per candidate
- [ ] Inference $/day computed
- [ ] Recommendation with sacrifice statement
- [ ] csam_adjacent defended separately
- [ ] Sprint 3: fusion arch compute-cost delta computed
- [ ] Awaiting my approval to promote

**Next file:** [`phase-06-metric-threshold.md`](./phase-06-metric-threshold.md)
