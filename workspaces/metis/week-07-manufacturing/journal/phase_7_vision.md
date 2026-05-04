<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 7 — Red-Team · Vision QC

**Decision moment:** Probe the vision QC inspector for failure modes before promoting to production.
**Sprint:** 1 (Vision QC)
**Time:** 18:14
**Artefact produced:** `journal/phase_7_vision.md`

## Five dimensions

- **D1 Harm framing** — vulnerabilities slip past Phase 6 into shadow if we don't deliberately probe. Adversarial classes (e.g. flux residue mistaken for solder bridge) cost $620 per cold-start misclassification.
- **D2 Metric → cost linkage** — robustness probes drive Phase 13 retrain rules. A failure mode found at Phase 7 = a drift signal we know to monitor in Sprint 4.
- **D3 Trade-off honesty** — exhaustive adversarial probing is unbounded; the gate is "find the obvious failures, not all failures."
- **D4 Constraint classification** — WSH 0.40 floor is enforced server-side; verified at the boundary returns 409 (not bypassable from the client).
- **D5 Reversal condition** — any probed failure mode that exceeds 5% prevalence on the live shadow window → freeze chosen arch and retrain.

## What I probed

1. **Sub-floor threshold injection.** `POST /inspect/vision/threshold {class:"safety_critical_defect", threshold:0.20}` → 409 with WSH-cited error. Defense holds.
2. **Sub-floor promotion.** Set safety_critical to 0.40 (boundary), then promoted to shadow → 200. Set safety_critical to 0.20 (below floor), then promoted → 409 (defensive double gate). Defense holds at both threshold POST and promote POST.
3. **Per-class confusion matrix on chosen arch.** ResNet macro F1=0.98; lowest per-class is major_defect at 0.95. Brier 0.0054 on major_defect — well-calibrated; no posterior collapse.
4. **Cohort skew check.** Class 3 boards (60%) and Class 2 boards (40%) — chosen arch macro F1 holds within 0.02 across the two cohorts (no per-IPC-class drift).
5. **Adversarial defect-mode probe.** `solder_bridge` and `missing_component` are dominant in major + safety classes; `flux_residue` and `conformal_coating_bubble` are NOT in training data → cold-start risk identified.

## What surfaced

The chosen arch (ResNet-50) is robust on the 7 known defect modes. Cold-start exposure is the dominant residual risk: novel defect modes appearing in the wild will route to "good" with high confidence, masking $620/incident escalation. Phase 13 must monitor the per-class score-distribution drift (PSI on the leaderboard outputs) to catch novel-mode appearance before it cascades.

## What I am promoting anyway

ResNet-50 to shadow stage. The 0.98 macro F1 is well above the 0.78 AOI baseline (the floor to beat); the 7-day shadow window will surface novel modes before production promote. Risk-acceptance: cold-start exposure on novel modes is the price of shipping today; mitigation = drift monitor at Phase 13.

## Reversal condition

Per-class FN rate trend > 0.05 for 7 days OR appearance of a novel defect mode at > 5% prevalence on shadow → freeze + retrain.

## Risks I am accepting

Cold-start cost on novel defect modes ($620/incident, expected ~2-4 incidents/quarter based on prior-year mode-introduction rate). Frozen-backbone transfer cannot adapt to a new mode without re-fitting the head; `POST /inspect/vision/train` re-fits the head deterministically per seed, so the recovery path is < 1 day if a novel mode is identified.
