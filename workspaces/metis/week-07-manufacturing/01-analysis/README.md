<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# `/analyze` Output — Week 7 Manufacturing

`/analyze` is short tonight (~10 minutes). The product is pre-built. Your only job in this phase is to declare, in writing, the boundary between what the scaffold has already committed to (Vision QC + PredMaint + RL + Agent harness + drift baselines × 3) and what remains for the 14 Playbook phases to decide.

## Files produced here

- `failure-points.md` — 12 ways the LumenCircuit industrial AI suite could fail in production (3 per module × 4 modules). Each one cites a specific `src/manufacturing/backend/routes/<file>.py::<function>` location and maps to the Playbook phase that catches it. If you cannot name a Playbook phase that catches it, you have discovered a gap in the Playbook (flag to the instructor).
- `assumptions.md` — what the pre-built baseline already assumes. ResNet-50 / EfficientNet-B0 / ViT-Small as the three vision heads (transfer-learning, frozen backbones). LightGBM / LSTM / Survival Forest as the three predictive-maintenance families. PPO / DQN / Random as the three RL policies. Drift cadences hardcoded as vision-weekly / sensor-daily / RL-per-deployment. Every assumption you accept tonight is a decision by omission.
- `decisions-open.md` — the inverse: what remains open for you to decide in Sprints 1–4. Per-class vision thresholds × 4, predmaint window pick, RL reward function weights × 4, agent autonomy ladder, MOM/WSH hard-shadow re-run, three retrain rules at three cadences.

## Guiding questions

1. **What does the pre-built baseline commit to?** Read `/inspect/vision/leaderboard`, `/predict/maintenance/leaderboard`, `/optimize/rl/leaderboard`, `/agent/policy`, `/drift/retrain_rule/{vision,predmaint,rl}`. What numbers and architectures are already baked in?
2. **What would a hostile Head of Quality ask about this baseline?** (Hint: she will ask about per-class recall on `safety_critical_defect` first, then the 49:1 asymmetry math.)
3. **What would hostile Head of EHS ask?** (Hint: WSH Act 2006, MOM Inspectorate audit, the agent autonomy ladder, the $50K equipment-damage envelope, and what counts as "shadow" when the MOM mandate fires.)
4. **What would a hostile Head of Operations ask?** (Hint: 7-day prediction window, $12,000 unplanned-stop vs $1,800 planned-stop math, queue depth, and what the $35/min inspector pool looks like at peak Q4 ramp.)
5. **What would Legal Counsel ask?** (Hint: audit-trail completeness for every auto-decision, IPC-A-610 Class 3 contractual flow-through, and the $1M WSH ceiling.)
6. **Which of the five Trust Plane decision moments from `PRODUCT_BRIEF.md §"The five Trust Plane decision moments"` are already resolved, and which are still yours?**

## Gate to `/todos`

Your `failure-points.md` must name at least 12 distinct failure modes (3 per module × 4 modules), each cited to a `src/manufacturing/backend/routes/<file>.py::<function>` location and each mapped to the Playbook phase that catches it. Any module under-represented or any phase left unmapped → `/analyze` re-runs. No `/todos` start until the gate passes.
