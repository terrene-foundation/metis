# Phase 1 — Frame

**Sprint:** 1 · **Time:** **_:_** · **Artefact:** `journal/phase_1_frame.md`

## Target / output

<One sentence: precise, not fuzzy. e.g. "5-class auto-decision per image post under 60-second latency for csam_adjacent and 90-min SLA for other classes">

## Population

- **Inclusions:** <e.g. all image+text posts from active accounts in SG/MY/ID/PH/TH>
- **Exclusions:** <e.g. internal test accounts, system-generated reposts, posts already auto-removed by rule layer>

## Horizon / latency window

<e.g. 60s for CSAM-adjacent (IMDA-mandated), 90-min SLA on standard human-review queue>

## Cost asymmetry (cite PRODUCT_BRIEF.md §2)

- **Primary cost term:** $\_\_\_ per \_\_\_ ← false negatives (harmful left up)
- **Secondary cost term:** $\_\_\_ per \_\_\_ ← false positives (legitimate auto-removed)
- **Daily-volume anchor:** $\_\_\_ × \_\_\_ volume = $\_\_\_/day at risk
- **Structural floor (separate):** IMDA $1M ceiling on csam_adjacent

## Throughput ceiling

- **Value:** \_\_\_ posts/min auto-decision
- **Owned by:** \_\_\_ (Reviewer Ops Lead / Head of T&S — name the role)
- **Sourced from:** \_\_\_ (brief / scaffold config / stakeholder interview)

## What would flip my mind (D5)

<Specific signal + threshold + duration. "If reviewer headcount drops below N for 2 weeks, tighten auto-remove threshold by 0.05.">

## Risks I'm accepting

<1–3 lines. Name the failure mode tonight's scope tolerates.>
