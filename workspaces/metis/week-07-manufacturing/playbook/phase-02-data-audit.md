<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 2 — Data Audit

## 1. What this phase decides

Read the labelled inspection dataset, sensor stream, and RL episode cache before any model trains, surfacing the six categories of trouble that wreck industrial-AI pipelines: label quality, leakage, survivorship, distribution shift, missingness, proxy variables.

## 2. The Week 7 lens

**Vision QC dataset (`boards_labelled.csv`, 800 rows):**
Inter-inspector agreement (Cohen's kappa) on the 100-board double-labelled subset. The boards auto-removed by AOI never reached human label — the labelled distribution is biased toward "boards AOI was uncertain about" (the survivorship gap is real and quantifiable: 12,000 daily inspection events vs 800 labelled = 15:1 selection ratio).

**Sensor stream (`sensor_stream.csv`, 432K rows):**
Per-machine missingness pattern (do all 10 machines have continuous coverage?), temporal leakage (`failure_event_time` cannot leak into the feature window — confirm sliding window ends BEFORE the labelled event), per-line and per-shift distribution shift (Line 1 vs Line 3 supplier-lot mix), per-machine cohort balance (4 of 10 machines have a labelled failure; 6 do not — extreme imbalance).

**RL episodes (`rl_episodes.json`, 30K transitions):**
Episode label quality (was the safety_violation flag computed correctly per episode?), survivorship (only "successful" rollouts cached or also crash-terminated ones?), distribution shift (does the cached state distribution match what production would see?).

**Safety images (`images_safety/`, 200 rows):**
Hand-labelled — kappa is 1.0 by construction but the population is the surface to scrutinise (PPE/no-PPE × restricted-zone/clear is a 2×2 grid; balance matters).

## 3. Your levers

- **Per-class kappa** — which class has the worst inter-inspector agreement? That is your highest Phase 6 threshold risk
- **Per-machine sensor coverage** — gaps create silent FN risk in predmaint
- **Per-line / per-shift distribution** — Phase 7 cohort sweep starts here
- **Survivorship gap quantification** — AOI selection ratio in vision; healthy-machine population in predmaint
- **Proxy variable flag list** — line_id and shift correlate with operator cohort (a manufacturing analog to demographic proxy)

## 4. Paste-ready block for the journal

```
I'm in Playbook Phase 2 — Data Audit. The vision moderator trains on
labelled inspection data; the predmaint classifier trains on sensor
windows; the RL policy trains on cached transitions. I need a six-category
audit BEFORE training:

1. Label quality — what's the inter-inspector agreement on the 100-board
   double-labelled subset (Cohen's kappa per class)? Where do inspectors
   disagree most?
2. Temporal leakage — is the predmaint feature window strictly BEFORE
   the labelled failure_event_time? Confirm the sliding window endpoint
   for each of the 4 failing machines.
3. Survivorship bias — how many boards/day does AOI auto-remove (didn't
   reach human label)? Quantify the labelled-vs-actual selection ratio.
4. Distribution shift — does the labelled set look like the live stream?
   Per-line (Line 1 / 2 / 3), per-shift (day/swing/night), per-supplier-
   lot balance.
5. Missingness pattern — per-machine sensor gaps. Are missingness patterns
   correlated with the labelled failure event?
6. Proxy variables — line_id and shift correlate with operator cohort.
   supplier_lot_id correlates with component vendor. Flag these.

For each category, name 2–3 specific findings with row counts. Cite the
file. If you cannot cite a file, say "I have not read this — confirming
required."

Tonight-specific:
- Source datasets: src/manufacturing/data/boards_labelled.csv (800 rows),
  sensor_stream.csv (432k rows ≈ 30 days × 10 machines × 1-min cadence),
  rl_episodes.json (30k transitions across 3 policies).
- Label-quality: Cohen's kappa per class on the 100-board double-labelled
  subset. Safety_critical_defect typically has lowest kappa (rarer class
  + more inspector disagreement on borderline cases). Worst-kappa class
  is your highest Phase 6 threshold risk.
- Temporal leakage: predmaint sliding window MUST end ≥ 1 minute before
  failure_event_time. Confirm for each of the 4 failing machines.
- Survivorship: 12,000 inspection events/day vs 800 labelled boards =
  ~15:1 selection ratio. AOI biases the labelled set toward "boards AOI
  was uncertain about." Quantify the survivorship gap.
- Distribution shift: 3 SMT lines × 3 shifts. Do the 800 labelled boards
  cover all 9 line-shift cells? Are some shifts under-represented?
- Missingness: do all 10 machines have full 30-day coverage at 1-min
  cadence? Per-machine row count must be ≈ 43,200.
- Proxy variables: line_id + shift correlate with operator cohort
  (manufacturing analog to demographic proxy). supplier_lot_id correlates
  with component vendor and may be a proxy for source-quality.

Do NOT propose remediations beyond "drop", "log", or "investigate".
Remediation is my call.
Do NOT use "blocker" without a named next step.

Journal file: copy journal/skeletons/phase_2_data_audit.md into
workspaces/metis/week-07-manufacturing/journal/phase_2_data_audit.md.

When the journal file has all six categories with findings, stop.
```

## 5. Cost anchor

From `specs/business-costs.md`:

- A label-quality finding on safety_critical_defect propagates to Phase 6 threshold setting → directly affects the $1M+ WSH exposure
- A survivorship gap on AOI-selected boards propagates to Phase 5 implications → defending a chosen architecture against an unbiased population is impossible if the population is biased
- A per-machine sensor gap propagates to Phase 6 PredMaint threshold → wrong threshold on a partially-blind machine costs $12,000 / unplanned stop

## 6. Hard-floor table

Not directly applicable — Phase 2 surfaces data quality findings; floors apply at Phase 6 / 11 where decisions get made on top of the data.

## 7. Reversal condition

A Phase 2 audit is reversed when:

- **Signal**: a Phase 7 robustness finding traces back to a Phase 2 finding the audit waved away as "minor"
- **Threshold**: any single finding with blast-radius > $50K/year that the audit didn't quantify
- **Duration**: discovered at /redteam — re-open Phase 2 immediately

## 8. Transfer to next project

The six categories are universal to ML data work. In any new domain: (a) inter-labeller agreement on a held-out double-labelled subset; (b) temporal leakage check on every feature; (c) survivorship gap quantification; (d) distribution shift across natural cohorts (line/shift/supplier here, market/segment/cohort elsewhere); (e) missingness patterns and their correlation with the label; (f) proxy-variable flags. The order above is the order: audit before features, features before model.

---

**Next file:** [`phase-03-features.md`](./phase-03-features.md)
