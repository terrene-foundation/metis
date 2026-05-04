<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 1 — Frame

**Decision moment:** What is THIS workshop's product trying to do, for whom, against which costs, with which constraints hard-floored?
**Sprint:** 1 (Vision QC) — shared framing across all four sprints
**Time:** 17:59
**Artefact produced:** `journal/phase_1_frame.md`

## Five dimensions

- **D1 Harm framing** — LumenCircuit (Singapore PCBA, IPC-A-610 Class 3, BizSAFE Lvl 4) contracts to medical-device, automotive ADAS, and aerospace customers. The Q1 2026 aerospace recall cost S$3.2M; field-return defects cost $4,200/board on average, while a single WSH-notifiable incident carries criminal director liability + $1M+ fine.
- **D2 Metric → cost linkage** — headline metric is per-class precision/recall on the 4-class vision inspector + per-window F1 on the predmaint classifier. Linkage: FN × $4,200 + FP × $85 → 49:1 asymmetry. Symmetric metrics (raw accuracy) systematically under-price missed safety-critical defects.
- **D3 Trade-off honesty** — shipping AOI 78% recall is "good enough" only if you accept that 22% of true defects ride out to medical-device customers. The product replaces AOI rule-based triage with ML-assisted triage routing the ambiguous 12k events/day post-AOI.
- **D4 Constraint classification** — HARD: safety_critical_defect threshold ≥ 0.40 (IPC-A-610 + WSH); RL safety_penalty ≥ floor that yields 0 violations on cached rollouts; equipment damage envelope $50K; restricted-zone access 0 incursions; line speed ≤ 60 boards/min and reflow zone ≤ 250 °C when MOM mandate active. SOFT: queue depth, throughput target (~$48k-72k/day recovery), reviewer headcount.
- **D5 Reversal condition** — customer-mix shift (e.g. > 25% non-Class-3 contracts) → re-evaluate WSH floor. New defect-mode appearing with > 0.05 base rate → retrain trigger AND threshold review.

## What I decided

The four modules in scope are vision QC (transfer learning), predictive maintenance (time-series ML), process optimisation (RL on reflow oven), and a coordination agent with drift × 3 monitors. The 49:1 defect-shipped vs false-scrap asymmetry is the headline framing constraint; the WSH $1M ceiling sits structurally above any cost-balanced threshold and is non-optimisable.

## Why (in business terms)

LumenCircuit has 12,000 inspection events/day post-AOI. At $35/min × 1,400 boards × 3-min mean review = $147,000/day in inspector cost; that is the ceiling on what the product can shift back to humans. The 22% AOI recall gap × major-defect base rate × $4,200 = exposure that the ML-assisted triage must close. The MOM/WSH regulatory pressure is the operating envelope: any agent action affecting safety must be in shadow until cleared.

## What I rejected

"Just tune AOI thresholds" — would not address the $4,200/board recall risk on novel defect modes. "Roll a single global model across all 4 classes" — silently averages the 49:1 asymmetry with the 2:1 minor-defect asymmetry, mis-prices safety-critical-class FN.

## Reversal condition

Customer-mix shifts away from IPC-A-610 Class 3 (more general industrial work) → re-evaluate the 0.40 WSH floor and the 49:1 framing. New defect mode appearing in the wild with > 0.05 base rate → retrain trigger.

## Risks I am accepting

800 labelled images is small for transfer learning; novel defect modes cold-start cost is $620/incident. The 10-machine sample for predmaint constrains per-machine differentiation. Cached RL rollouts assume the reflow-oven dynamics stay within the envelope the cached policies were trained on.
