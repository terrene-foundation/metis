<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 5 — Implications (pick the candidate)

## 1. What this phase decides

Read the Phase 4 leaderboard and pick the candidate to ship — defended in $ of cost-asymmetry × per-class metrics + calibration + edge-latency feasibility (vision) / window-trade-off (predmaint) / hard-floor compliance (RL).

## 2. The Week 7 lens

**Vision pick (Sprint 1):**
The architecture decision is partly an edge-deployment trade-off (80 ms/board on Jetson). EfficientNet-B0 typically wins on inference cost; ViT-Small wins on accuracy but is data-hungry at 800 images; ResNet-50 is the robust middle. The pick must defend against (a) per-class P/R/F1 weighted by 49:1 asymmetry, (b) Brier per class, (c) inference cost at $0.001/board × 12,000 boards/day, (d) the 80 ms latency ceiling.

**PredMaint pick (Sprint 2):**
Two decisions in one: which family AND which prediction window. Family choice is on cost-asymmetry-weighted F1 + calibration. Window choice is on the trade-off between FP rate (planned-maintenance overhead at $1,800/window) and FN rate (missed signal → unplanned stop at $12,000). 7-day window is the operations sweet spot — you defend whichever you pick.

**RL pick (Sprint 3):**
Pick a policy from `/optimize/rl/leaderboard` (PPO / DQN / Random) on the four reward dimensions (throughput / defect / energy / safety). The pick is constrained by the hard-floor table — any policy with non-zero hard-floor violations across 10,000 episodes is BLOCKED from promotion regardless of throughput score.

## 3. Your levers

- **Cost-asymmetry-weighted score** — the leaderboard's F1 is not the answer
- **Calibration as tiebreaker** — when two candidates tie on F1, lower Brier wins
- **Inference-cost ceiling** — $/day at the daily volume must fit within compute budget
- **Edge-latency feasibility (vision)** — the 80 ms/board ceiling is hard
- **Window choice (predmaint)** — defended in $ of $12K-vs-$1.8K asymmetry
- **Hard-floor pass (RL)** — any candidate with non-zero violations is BLOCKED

## 4. Paste-ready block for the journal

```
I'm in Playbook Phase 5 — Implications. Read data/leaderboard.json (the
relevant sprint's leaderboard). For each candidate compute:

1. Cost-asymmetry-weighted score: ($FN cost × per-class FN rate) +
   ($FP cost × per-class FP rate), summed across classes
2. Calibration: Brier score per class
3. Inference-cost: $/day at the daily volume

Recommend ONE candidate. Defend in 1–2 paragraphs:
- What you sacrificed by NOT picking each other candidate
- Why this candidate's calibration is acceptable for the downstream
  consumer (queue allocator / maintenance scheduler / agent)
- Why inference cost is feasible at the daily volume
- (Sprint 1 only) Why edge-latency is met under the 80 ms ceiling
- (Sprint 2 only) Why the chosen prediction window is right under
  the $12K-vs-$1.8K asymmetry
- (Sprint 3 only) Why the policy clears the hard-floor table

Do NOT promote without me approving the recommendation.
Do NOT use "blocker" without specifics.

Sprint detection:
- Sprint 1 (Vision): pick architecture (resnet50 / efficientnet / vit)
- Sprint 2 (PredMaint): pick family AND prediction window
- Sprint 3 (RL): pick policy (ppo / dqn / random)

For Sprint 1:
- Cost asymmetry: $4,200 FN / $85 FP (49:1) — cite specs/business-costs.md
- Daily volume: 12,000 inspection events/day
- Edge inference: $0.001 per board, 80 ms/board on Jetson — cite §4.1 + §7
- Inference-cost feasibility: candidate × 12,000/day × $0.001 = $12/day
  (vision is cheap; the binding constraint is latency, not cost)
- WSH ceiling on safety_critical_defect: hard floor 0.40, NOT cost-balanced.
  Phase 5 must defend safety_critical SEPARATELY from cost-balanced math.

For Sprint 2:
- Cost asymmetry: $12,000 FN / $1,800 FP (6.7:1) — cite specs
- Volumes: 10 machines × 1 check/day = 10 daily; rare event (4 of 10 had
  failures in 30 days)
- Window trade-off: 3 days = faster recovery, more FP; 7 days = ops sweet
  spot; 14 days = lower FP but throughput already lost. Defend in $/day
  via expected (FN × $12K + FP × $1.8K) at each window.
- Calibration: scheduler consumes probabilities → Brier ≤ 0.20 floor

For Sprint 3:
- Reward function: weighted combo of throughput / defect_cost / energy /
  safety. Defended in Phase 7 RL (Goodhart leaderboard).
- Hard floors (cite specs/compliance-floors.md): safety_penalty weight ≥
  floor that yields 0 hard-floor violations across 10,000 episodes;
  equipment-damage envelope $50K (0/year); WSH-notifiable 0/year.
- Any policy with non-zero hard-floor violations is BLOCKED from
  promotion regardless of throughput.

Journal file: copy journal/skeletons/phase_5_implications.md (suffix by
sprint: _vision / _predmaint / _rl).
```

## 5. Cost anchor

From `specs/business-costs.md`:

- **Sprint 1**: $4,200 FN × per-class FN rate + $85 FP × FP rate. Edge inference $0.001/board × 12,000 boards/day = $12/day (negligible vs FN cost).
- **Sprint 2**: $12,000 unplanned vs $1,800 planned. The 6.7:1 asymmetry tilts toward catching failures; the binding decision is window length.
- **Sprint 3**: throughput recovery target $48,000–$72,000/day at 2-3% lift × 40,000 boards/day × $60 contribution margin. Compute cost $0.40/training-hour × ~6 hr/week = $2.40/week (negligible).

## 6. Hard-floor table

Sprint 5 (Vision): the 0.40 floor on safety_critical_defect lives at Phase 6, not Phase 5 — but Phase 5 MUST acknowledge it explicitly when defending the chosen architecture (a high-Brier candidate makes the 0.40 floor noisier).

Sprint 5 (RL): every candidate's leaderboard row has a `safety_violations` count. Any non-zero count is a hard BLOCK from Phase 5 promotion regardless of throughput.

## 7. Reversal condition

A Phase 5 pick is reversed when:

- **Signal**: a Phase 7 robustness finding shows a candidate that wasn't picked is materially more robust
- **Threshold**: per-class recall delta > 5 pp on the chosen-but-vulnerable class
- **Duration**: any single Phase 7 sweep

Then re-open Phase 5 — the leaderboard read missed a robustness dimension.

## 8. Transfer to next project

The four-axis evaluation (cost-asymmetry × calibration × inference-cost × hard-floor) generalises. In any new domain, replace "edge-latency" with whatever the deployment surface's binding constraint is (cloud cost, mobile RAM, query latency); replace "window choice" with whatever the temporal trade-off is (forecast horizon, batch frequency); keep the hard-floor pass as the structural defense against shipping a high-throughput model with regulator exposure.

---

**Next file:** [`phase-06-metric-threshold.md`](./phase-06-metric-threshold.md)
