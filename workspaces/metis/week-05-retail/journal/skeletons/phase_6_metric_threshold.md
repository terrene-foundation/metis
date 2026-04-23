# Phase 6 — Metric + Threshold

**Sprint:** 1 (USML — three floors) or 2 (SML — threshold on PR curve) · **Time:** **_:_**

---

## USML variant (Sprint 1)

### The three floors — COMMITTED BEFORE seeing Phase 4 leaderboard (timestamp **_:_**)

- **Separation floor:** silhouette ≥ **_ (historical variance grounding: _**)
- **Stability floor:** bootstrap Jaccard ≥ \_\_\_ (convention 0.80 unless defended)
- **Actionability floor:** \_\_\_ (test: can marketing name one distinct action per segment?)

### Chosen operating point

- **K =** **_ · **Algorithm =** _**

### Counterfactual dollar lift vs incumbent (D2)

- Current rule-based system: \_\_\_% correct-segmentation baseline
- New system: \_\_\_% correct-segmentation on hold-out
- Lift: **_ customers × $45 saved-or-earned = **$_**/month\*\*

### Reversal condition (D5)

- **Signal:** \_\_\_
- **Threshold:** \_\_\_
- **Duration:** \_\_\_
- _(e.g. "if bootstrap Jaccard drops below 0.80 for 2 consecutive monthly re-clusters, drop back to K-1")_

### Risks accepted

<What floor value is generous? Defend it. "Set separation floor at 0.25 because Arcadia's historical behavioural variance produces ~0.20–0.30 baseline; pre-registering at 0.25 picks up meaningful structure without demanding synthetic neatness.">

---

## SML variant (Sprint 2)

### Primary metric

- ROC-AUC / PR-AUC / F1 / precision@recall-X / calibrated-Brier: \_\_\_
- **Reason:** \_\_\_ (rare positives → PR; balanced classes → ROC; etc.)

### Cost asymmetry (D1)

- **Cost per false negative:** $\_\_\_
- **Cost per false positive:** $\_\_\_
- **Ratio:** \_\_\_:1 (favours: recall / precision)

### Chosen threshold (D2)

- **Threshold:** \_\_\_ (chosen on PR / ROC curve)
- **Expected cost at threshold:** $\_\_\_ per 1,000 predictions
- **Recall at threshold:** **_ · **Precision at threshold:** _**

### Calibration

- Brier score: \_\_\_
- Recalibration applied (Platt / isotonic / none): \_\_\_

### Class imbalance handling

- Stratified CV / class weights / SMOTE / none: \_\_\_

### Reversal condition (D5)

- **Signal:** **_ · **Threshold:** _** · **Duration:** \_\_\_
