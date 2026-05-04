<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 5 — Implications · Vision QC ★ (Trust-Plane decision moment 1 of 5)

**Decision moment:** Which vision QC architecture do we promote (ResNet / EfficientNet / ViT)?
**Sprint:** 1 (Vision QC)
**Time:** 18:08
**Artefact produced:** `journal/phase_5_vision.md` + `POST /inspect/vision/promote {arch:"resnet50_lr_head", to_stage:"shadow"}`

## Five dimensions

- **D1 Harm framing** — picking a data-hungry architecture at 800 imgs ships under-trained recall, exposing $4,200/board on every missed defect routed past the inspector.
- **D2 Metric → cost linkage** — macro F1 differential × 12,000 events/day × major-defect base rate (10%) × $4,200 = $/day at stake. ResNet F1=0.98 vs ViT F1=0.32 means choosing wrong = ~792 missed defects/day at the major-defect class alone.
- **D3 Trade-off honesty** — chose ResNet not EfficientNet despite EfficientNet being marketed as "edge-friendly". The 0.46 F1 gap (0.98 vs 0.52) outweighs the marginal MFLOPS savings; on Jetson Nano both run within the 80ms budget on 32×32 inputs.
- **D4 Constraint classification** — IPC-A-610 Class 3 100% inspection coverage is HARD; chosen arch must hit every board.
- **D5 Reversal condition** — labelled image count > 5,000 AND ViT macro_f1 closes to within 0.05 of ResNet → re-evaluate.

## What I decided

Promoted `resnet50_lr_head` (macro_f1=0.9801, embed_dim=32) from `staging` to `shadow`. Per-class breakdown on the chosen arch:

| Class                    | Precision | Recall | F1     | Brier  | Base rate |
| ------------------------ | --------- | ------ | ------ | ------ | --------- |
| good                     | 0.9921    | 0.9921 | 0.9921 | 0.0059 | 0.635     |
| minor_defect             | 0.9783    | 0.9783 | 0.9783 | 0.0060 | 0.230     |
| major_defect             | 0.9500    | 0.9500 | 0.9500 | 0.0054 | 0.100     |
| safety_critical_defect   | 1.0000    | 1.0000 | 1.0000 | 0.0004 | 0.035     |

The safety_critical_defect class has perfect P/R/F1 on the held-out set — Brier 0.0004 is the calibration evidence. This is the structural defense for the 0.40 WSH floor at Phase 6.

## Why

ResNet-50 wins at 800-image scale because the conv inductive bias transfers cleanly from ImageNet textures to PCB-defect textures. ViT-Small loses (F1=0.32) because attention needs ~10× the data to specialise. EfficientNet-B0 lands in the middle (F1=0.52); the marginal latency saving on Jetson does not justify the F1 loss. Per `playbook/phase-05-implications.md`, the chosen architecture also drives downstream choices: edge deployment uses ResNet's 32d embedding for the shadow-mode A/B comparison.

## What I rejected

ViT — under-trained at 800 imgs. Cite: macro_f1=0.32 on the held-out set; 0.66 gap to ResNet. EfficientNet — middle-of-the-leaderboard 0.52; choosing it for marginal latency would surrender 0.46 F1 for negligible inference cost savings on the volume.

## Reversal condition

If next-quarter labelled count grows past 5,000 AND ViT macro_f1 reaches within 0.05 of ResNet on a fresh holdout → re-evaluate. Brier on safety_critical_defect drifting > 0.05 over 14 days → demote to staging + retrain.

## Risks I am accepting

Frozen-backbone transfer may miss a defect mode the ImageNet pre-training never saw (e.g. flux residue, conformal-coating bubbles); cold-start cost $620/incident. Promoted to shadow only — production promotion deferred until 7-day shadow-period FN rate is < 0.05 on the safety_critical_defect class.
