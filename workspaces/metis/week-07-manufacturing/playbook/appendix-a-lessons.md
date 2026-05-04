<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Appendix — Transferable lessons accumulating through the term

_(Populated by Phase 9 Codify at the end of each week.)_

### Week 4 (supply chain / SML + optimization)

- AutoML trials above 10 blow the Sprint 1 budget and add no discovery value.
- "Monitor production" means nothing; "monitor [signal] weekly, alert at [threshold]" is the contract.
- Cost asymmetry in $ anchors every later phase; without it, floors float.

### Week 5 (retail / USML + SML + Opt + MLOps)

- Pre-registered floors (silhouette, stability, actionability) only mean something if written before the leaderboard. Post-hoc floors score 0.
- Two segments with the same downstream marketing action are one segment with noise — collapse, don't ship two.
- The PDPA injection demands BOTH a Phase 11 re-classification AND a Phase 12 re-solve. Skipping the re-solve is the single most common D3 zero.

### Week 6 (content platform / CNN + Transformer + Multi-modal + MLOps × 3 cadences)

- Per-class threshold setting is structurally different from a single threshold — 5 classes = 5 different cost-balanced points + 1 hard regulator floor.
- Joint-embedding fusion catches cross-modal patterns but at ~3× compute; the pick is justified in coverage gain × $ vs compute-cost delta, not "best-in-general."
- Three drift cadences (image weekly / text daily / fusion per-incident) stratify by modality; universal cadences fail.

### Week 7 (manufacturing / Transfer Learning + Time-series + RL + Agent + MLOps)

**Live numbers from the 2026-05-04 walkthrough end-state — students inherit these as the "after picture" they study before running their own pass.**

- **Transfer learning at small scale: simpler arch wins.** ResNet-50 macro_f1=0.9801 beat EfficientNet-B0 (0.5180) and ViT-Small (0.3249) at 800-image scale. The "just use the SOTA arch" instinct loses when the data is small; conv-inductive-bias transfers cleaner than attention.
- **Per-class hard floors are the structural defense, not the cost calc.** safety_critical_defect threshold is 0.40 because IPC-A-610 + WSH say so, NOT because the cost math computed it. Major_defect at 0.30 IS cost-balanced (49:1 asymmetry pulls it low). Thinking these two are the same kind of decision is the trap.
- **RL reward weights live in $-space, not loss-space.** Chosen weights (throughput=1, defect_cost=10, energy_cost=0.1, safety_penalty=1.0) reflect that one defect costs ~10× one minute of throughput. safety_penalty=1.0 sits 2× above the empirically-derived hard floor 0.50 — defense in depth at 0.03 throughput-points cost.
- **Pre-MOM vs post-MOM constraint reclassification matters.** Line-speed 60 / reflow-temp 250 are SOFT (envelope guidance) pre-MOM, HARD (rejection gates) post-MOM. The PPO policy that promotes cleanly to shadow pre-MOM has 14.4% line_speed-violating rollouts that block production-promotion post-MOM. Compliance shadow price ≈ $15-28k/day; document for legal counsel.
- **The MOM injection touches three endpoints, not one.** `/agent/policy` (forced shadow on WSH-affecting), `/optimize/rl/simulate` (hard_floor_active flips true), `/state/current` (mom_mandate_active flag for the viewer). Skipping any one of the three is a D3 zero on the rubric.
- **Three drift cadences match three data-generating processes.** Vision weekly (equipment + supplier drift), predmaint daily (sensor + calibration drift), RL per-deployment (envelope + reward shape changes). Universal "weekly retrain" wastes compute and misses the fast cadences.
- **Inspector queue LP allocator earns its compute.** Solved a 3-tier critical/major/minor allocation in milliseconds with $1,445,220/shift net catch value and -$120/min shadow price (each marginal inspector-minute would catch $120 more). The LP is also the auditable defense at Phase 11 — every constraint is named with hard/soft tag and dollar penalty.

**Five ★ Trust-Plane decisions — the actual values committed in the walkthrough:**

1. Vision arch: `resnet50_lr_head` (macro F1 0.9801, embed 32d)
2. Per-class thresholds: good=0.50 / minor_defect=0.50 / major_defect=0.30 / safety_critical_defect=0.40 (WSH HARD)
3. PredMaint family + window: `lightgbm_features` at 7 days (Brier 0.0)
4. RL reward weights: throughput=1.0 / defect_cost=10.0 / energy_cost=0.10 / safety_penalty=1.0 (chose 1.0 not 0.50; defense in depth)
5. Agent autonomy ladder (under MOM mandate): vision_triage=recommend / maintenance_scheduling=recommend / setpoint_adjustment=shadow (forced) / safety_alert=shadow

**Three retrain rules persisted to `retrain_rules.json`:**

- vision: psi > 0.30, 7d duration, HITL first trigger, exclude q4_automotive_ramp + medical_certification_cycle
- predmaint: calibration_decay > 0.10, 3d duration, HITL first trigger, exclude q4_automotive_ramp
- rl: combined > 0.15, per_deployment, HITL first trigger, no seasonal exclusion

---
