# Phase 8 — Deployment Gate

**Sprint:** 1 (Vision) / 2 (Text) / 3 (Fusion) · **Time:** **_:_** · **Artefact:** `journal/phase_8_gate_<vision|text|fusion>.md`

## Pre-registered floors (recap from Phase 6)

- Per-class precision floor: ≥ \_\_\_
- Per-class recall floor on harm: ≥ \_\_\_
- Per-class Brier ceiling: ≤ \_\_\_
- csam_adjacent: hard-floor 0.40 (IMDA)

## Floor-by-floor verdict

| Floor  | Pre-registered value | Measured | PASS / FAIL |
| ------ | -------------------- | -------- | ----------- |
| \_\_\_ | \_\_\_               | \_\_\_   | \_\_\_      |

## HIGH-severity Phase 7 findings — disposition per finding

| Finding | Status (RESOLVED / ACCEPTED-WITH-MITIGATION) | Mitigation |
| ------- | -------------------------------------------- | ---------- |
| \_\_\_  | \_\_\_                                       | \_\_\_     |

## Inference-cost feasibility

- $/day at production volume: $\_\_\_
- Team budget ceiling: $\_\_\_
- Within budget? \_\_\_

## Overall verdict

**PASS** / **FAIL** — \_\_\_

## If PASS: promotion + rollback

- Promote to stage: **shadow** (default Phase 8 target — not production unless instructor accelerates)
- Endpoint fired: POST /moderate/<image|text|fusion>/promote with `{ version, to_stage: "shadow" }`
- Rollback signal (NAMED, monitorable): \_\_\_ (e.g. "image-class P/R drops below floor for 3 consecutive days")

## If FAIL: rerun plan

<Which floor failed, what changes for the rerun.>

## Sign-off

<I (the student) wrote PASS or FAIL above. The agent did not auto-promote.>
