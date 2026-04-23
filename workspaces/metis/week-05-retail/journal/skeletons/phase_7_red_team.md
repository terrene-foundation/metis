# Phase 7 — Red-Team

**Sprint:** 1 (USML segmentation) or 2 (SML classifier) · **Time:** **_:_**

## Transparency

- **Top features / important signals:** \_\_\_
- **Ablation impact when top feature dropped:** \_\_\_
- **Plain-language explanation of one output:** \_\_\_

## Robustness

- **3 worst subgroups:** **_ / _** / \_\_\_
- **3 worst conditions / time windows:** \_\_\_
- **Adversarial perturbation behaviour:** \_\_\_

## Safety (in $)

- **Worst-1% cost:** $\_\_\_
- **Degenerate-input behaviour:** \_\_\_
- **Blast radius (who gets hurt):** \_\_\_

## USML-specific probes (Sprint 1 only)

- **Re-seed Jaccard distribution across seeds:** [___, ___, ___] → mean **_, spread _**
- **Proxy-drop test:** dropping postal_district → \_\_\_% reassignment (shippable if < 30%)
- **Operational-collapse test:** smallest segment size on hold-out = **_ → risk: _**

## SML-specific probes (Sprint 2 only)

- **Calibration per subgroup:** **_ (max subgroup gap = _**)
- **Feature-ablation:** top feature dropped → AUC **_ → _**
- **Worst-quantile precision:** bottom 10% of predictions → precision \_\_\_

## Fairness

Deferred to Week 7 per Playbook. \_(One-line note of concerns spotted tonight that the Week 7 audit should take up: _\_\_)_

## Blockers

<None / list>

## Accepted risks (D3)

<Named trade-offs. What risk are we shipping with and why?>

## Mitigations to ship with

<What guardrails are in the Phase 8 gate?>

## Reversal condition (D5)

<What signal would escalate any accepted risk to blocker? e.g. "If any segment drops below 2% on next re-cluster, escalate to instructor.">
