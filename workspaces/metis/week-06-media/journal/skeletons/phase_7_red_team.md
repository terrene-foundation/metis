# Phase 7 — Red-Team

**Sprint:** 1 (Vision) / 2 (Text) / 3 (Fusion) · **Time:** **_:_** · **Artefact:** `journal/phase_7_red_team_<vision|text|fusion>.md`

## Findings (severity-ranked)

| #   | Sweep type             | Slice / perturbation                        | P/R/F1 delta vs holdout | Blast radius ($/year) | Severity (low/med/high) | Mitigation                              |
| --- | ---------------------- | ------------------------------------------- | ----------------------- | --------------------- | ----------------------- | --------------------------------------- |
| 1   | Adversarial            | <e.g. JPEG Q=30 on weapons class>           | \_\_\_                  | \_\_\_                | \_\_\_                  | <e.g. add JPEG aug to retrain pipeline> |
| 2   | OOD                    | <e.g. Bahasa Indonesia code-mixed>          | \_\_\_                  | \_\_\_                | \_\_\_                  | \_\_\_                                  |
| 3   | Demographic skew       | <e.g. per-class Brier varies by SEA market> | \_\_\_                  | \_\_\_                | \_\_\_                  | \_\_\_                                  |
| 4   | Cross-modal (Sprint 3) | <e.g. cute-puppy + harmful caption>         | \_\_\_                  | \_\_\_                | \_\_\_                  | \_\_\_                                  |
| 5   | \_\_\_                 | \_\_\_                                      | \_\_\_                  | \_\_\_                | \_\_\_                  | \_\_\_                                  |

## Three AI Verify dimensions covered

- **Transparency:** \_\_\_
- **Robustness:** \_\_\_
- **Safety:** \_\_\_

## Fairness (AI Verify dim 4) — DEFERRED to Week 7 per Playbook

<Mandatory line. Silent deferral scores 0 on rubric D4.>

## Risks accepted, not mitigated tonight

<1–3 lines per accepted risk. Each must reference (a) why mitigation is out of scope tonight, (b) the Phase 13 detection signal that will catch it in production.>

## Reversal condition (D5) — when does this assessment need redoing?

<Specific signal. "If JPEG-compression recall delta exceeds -3% on a Phase 13 weekly check, re-run Phase 7 adversarial sweep.">
