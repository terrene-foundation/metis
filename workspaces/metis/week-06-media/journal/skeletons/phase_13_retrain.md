# Phase 13 — Retrain Rules × 3 cadences

**Sprint:** 4 · **Time:** **_:_** · **Artefact:** `journal/phase_13_retrain.md` (single file, three rules inside)

## Rule 1 — Image Moderator (image_moderator) — WEEKLY cadence

- **Why weekly:** visual style moves slowly; drift is monotonic, not bursty
- **Signals:**
  - PSI on per-class score distribution
  - PSI on per-pixel-domain embedding feature
- **Threshold (variance-grounded from `drift_baseline.json`):**
  - Historical mean PSI: \_\_\_
  - Historical σ: \_\_\_
  - Threshold: mean + 3σ = \_\_\_
- **Duration window:** signal exceeds threshold for 2 consecutive weekly checks
- **HITL on first trigger:** YES (Reviewer Ops Lead approves)
- **Seasonal exclusion:** election cycles, major news events (cite PRODUCT_BRIEF.md §2)

## Rule 2 — Text Moderator (text_moderator) — DAILY cadence

- **Why daily:** language moves fast; slang and dogwhistles drift in days, not weeks
- **Signals:**
  - Token-frequency PSI on top-1000 tokens
  - Per-class calibration decay (Brier delta vs registered baseline)
  - Per-class score-distribution PSI
- **Threshold (variance-grounded):**
  - Historical mean: \_\_\_
  - σ: \_\_\_
  - Threshold: \_\_\_
- **Duration window:** signal exceeds threshold for 5 consecutive daily checks (1 week sustained)
- **HITL on first trigger:** YES
- **Seasonal exclusion:** election cycles, major news events

## Rule 3 — Fusion Moderator (fusion_moderator) — PER-INCIDENT cadence

- **Why per-incident:** adversaries probe joint seams in real time; only fires when complaints touch high-fusion-confidence posts
- **Signals:**
  - Cross-modal alignment-score variance vs registered baseline
  - Per-incident calibration check on the post that triggered the complaint
- **Threshold (per-incident):**
  - Variance > \_\_\_ OR Brier_complaint - Brier_baseline > \_\_\_
- **Aggregation rule:** if 5 complaints in 7 days exceed threshold, escalate to weekly review
- **HITL on first trigger:** YES
- **Seasonal exclusion:** election cycles, major news events (the spike in adversarial complaints would auto-trigger)

## Endpoint calls fired

- POST /drift/retrain_rule × 3 (one per model_id)
  - Image moderator: signals + threshold + duration + HITL + seasonal
  - Text moderator: same shape
  - Fusion moderator: same shape

## Why three cadences, not one universal (D3 — the trade-off)

<"A universal weekly cadence under-reacts on text (slang drifts in days, not weeks) and over-reacts on image (visual style moves slowly). Stratifying by modality cadence costs ~3× monitoring infrastructure ($X/year extra in compute) but prevents the silent text-moderator decay class of failure.">

## Reversal condition per rule (D5)

<For each rule: signal + threshold + duration that would change cadence or threshold. "If the text moderator runs 90 days with no trigger, consider relaxing daily to twice-weekly to save compute.">
