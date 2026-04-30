<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Decisions Still Open — MosaicHub Content Moderation

**Phase:** `/analyze` · **Author:** agent · **Date:** 2026-04-30
**Source:** intersection of `failure-points.md`, `assumptions.md`, and the 14-phase Playbook (`workspaces/metis/week-06-media/playbook/`).

What remains yours to decide tonight, organised by sprint and tagged to the Playbook phase that owns each decision. **No proposed values appear here** — the rubric demands you pre-register thresholds, weights, and architectures in their owning phase journals BEFORE seeing the leaderboard or the LP solve. A value proposed here would corrupt the pre-registration.

The five Trust-Plane decision moments (`PRODUCT_BRIEF.md §5`) are flagged ★. They are non-negotiable.

---

## Cross-sprint (shared framing)

| #   | Decision                                                                                                                                      | Owning phase | Notes                                                                                   |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | --------------------------------------------------------------------------------------- |
| C1  | ★ Define what counts as harmful — auto-remove vs human-review vs creator-warn mapping per class (5 image + 5 text)                            | Phase 1      | Decision 1 of 5. Policy decision, not technical.                                        |
| C2  | Population scope — inclusions and explicit exclusions (test posts, internal accounts, system-generated, already-auto-removed)                 | Phase 1      | Frame writes this in plain language.                                                    |
| C3  | Horizon — auto-decision latency target stated in seconds (NOT "fast")                                                                         | Phase 1      | Throughput ceiling owned by Reviewer Ops Lead.                                          |
| C4  | Cost-asymmetry framing — primary FN vs FP terms, plus IMDA structural ceiling acknowledged separately                                         | Phase 1      | Cite `PRODUCT_BRIEF.md §2` verbatim.                                                    |
| C5  | Six-category data audit on 80k labelled posts — label noise, leakage, class imbalance, OOD coverage, demographic skew, scaffold-coverage gaps | Phase 2      | Single audit covers image and text; multi-modal subset is 8k.                           |
| C6  | Feature framing — declared image features + augmentations + post metadata, declared text features (token / embedding / lexicon overlays)      | Phase 3      | Scaffold uses synthetic embeddings; the framing is the artefact, not the embedding fit. |

---

## Sprint 1 — Vision · CNN · See

| #   | Decision                                                                                                                 | Owning phase     | Notes                                                                                                                                                                                                    |
| --- | ------------------------------------------------------------------------------------------------------------------------ | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| V1  | CNN unfreeze depth — frozen-head only / partial-unfreeze (last 2 conv blocks) / full-unfreeze                            | Phase 4 (Vision) | Three families on the leaderboard; no from-scratch CNN.                                                                                                                                                  |
| V2  | Family pick — defended on per-class F1 + cost-balanced threshold, NOT macro-F1 alone                                     | Phase 5 (Vision) | F1.1 is the trap; pre-register the ranking criterion.                                                                                                                                                    |
| V3  | Calibration acceptance — Brier-pass / Brier-fail per class; flag any class above pre-registered Brier floor as a finding | Phase 5 (Vision) | A2 + reliability bins.                                                                                                                                                                                   |
| V4  | ★ Per-class auto-remove threshold × 5 image classes — `nsfw`, `violence`, `weapons`, `csam_adjacent`, `safe`             | Phase 6 (Vision) | Decision 2 of 5 (image half). 4 cost-balanced; CSAM hard floor at 0.40 already present (A2).                                                                                                             |
| V5  | Per-class POST `/moderate/image/threshold` action — `auto_remove`, `human_review`, `allow` per class                     | Phase 6 (Vision) | Don't conflate threshold with action — the route accepts any [0,1] for the threshold; action is encoded by which class+threshold combination triggers the dispatch in `routes/moderate_image.py::score`. |
| V6  | Phase 7 sweeps × 3 — adversarial pixel perturbation / OOD image robustness / demographic-skew                            | Phase 7 (Vision) | Names + acceptance criteria, executed via `/moderate/image/score` against curated holdouts.                                                                                                              |
| V7  | Sprint 1 deployment gate — PASS / FAIL on per-class evidence + threshold defense + red-team results                      | Phase 8 (Vision) | Promotion to shadow via `POST /moderate/image/promote`; both CSAM-floor gates apply.                                                                                                                     |

---

## Sprint 2 — Text · Transformer · Read

Phases 1–3 are NOT re-run. Phase 4–8 are replayed against the text moderator with `_text` suffix on the journal files.

| #   | Decision                                                                                                           | Owning phase     | Notes                                                                                         |
| --- | ------------------------------------------------------------------------------------------------------------------ | ---------------- | --------------------------------------------------------------------------------------------- |
| T1  | Family pick — fine-tuned BERT vs fine-tuned RoBERTa vs zero-shot LLM, defended on per-class F1 and per-class Brier | Phase 4–5 (Text) | A5; the 3-family leaderboard is at `/moderate/text/leaderboard`.                              |
| T2  | Calibration acceptance for the chosen text family — held-out reliability check, not in-sample (F2.2 is the trap)   | Phase 5 (Text)   | `routes/moderate_text.py::calibration` is in-sample.                                          |
| T3  | ★ Per-class auto-remove threshold × 5 text classes — `hate_speech`, `harassment`, `threats`, `self_harm`, `safe`   | Phase 6 (Text)   | Decision 2 of 5 (text half). All 5 cost-balanced; no IMDA floor on text classes (A2 + F2.1).  |
| T4  | `self_harm` dual-action declaration — auto-remove threshold AND a separate warn-and-queue threshold with helpline  | Phase 6 (Text)   | F2.1 — clinical-safety floor is non-negotiable; backend doesn't enforce it, journal must.     |
| T5  | Class-priority ordering at decision time — when a post crosses two thresholds, which class drives the action?      | Phase 6 (Text)   | F2.3; the route's positional default is `threats`/`self_harm` > others — declare or override. |
| T6  | Phase 7 sweeps × 3 — typo/unicode-confusable robustness / 5-market OOD (Singlish, Malay, code-mixed) / demographic | Phase 7 (Text)   | Acceptance criteria pre-registered before running the sweep.                                  |
| T7  | Sprint 2 deployment gate — PASS / FAIL + promotion to shadow via `POST /moderate/text/promote`                     | Phase 8 (Text)   | No CSAM-floor gate on this endpoint; calibration confirmation is the substitute.              |

---

## Sprint 3 — Fusion + Queue · Multi-Modal · Decide

Two products in one sprint: the fusion moderator's Phase 5 architecture pick, and the queue allocator's Phases 10–12.

| #   | Decision                                                                                                                                              | Owning phase          | Notes                                                                                    |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------- |
| F1  | ★ Fusion architecture — `early_fusion` / `late_fusion` / `joint_embedding`                                                                            | Phase 5 (Multi-Modal) | Decision 3 of 5. Defended on coverage gain × $ vs compute cost delta. A6 + F3.1.         |
| F2  | Fusion auto-route threshold — single threshold on `cross_modal_harm`; sets `auto_route_human_review` vs `allow`                                       | Phase 5 (Multi-Modal) | `POST /moderate/fusion/threshold`; default 0.50.                                         |
| Q1  | LP objective weights — `minimise_sla_breach` and `minimise_reviewer_cost` (must sum to 1.0)                                                           | Phase 10              | `POST /queue/objective`; the route enforces the sum.                                     |
| Q2  | Phase 11 first-pass constraints — hard set (reviewer headcount caps, qualified-pool restrictions) and soft set (SLA penalties, fatigue caps)          | Phase 11              | `POST /queue/constraints`; CSAM-adjacent stays SOFT in this pass.                        |
| Q3  | Phase 12 first-pass acceptance — feasibility, pathology check (tier starvation? pool over-utilisation?), accept / re-tune / fall back / redesign      | Phase 12              | `POST /queue/solve` returns the plan; viewer reads `last_plan`.                          |
| Q4  | ★ IMDA re-classification — `csam_adjacent` threshold, fusion threshold, and `imda_priority_must_clear_within_sla` flag (3 endpoints, F3.2)            | Phase 11 post-IMDA    | Decision 4 of 5 (re-class half).                                                         |
| Q5  | ★ IMDA queue re-solve — re-run `/queue/solve`, quantify `compliance_cost_imda` from the plan body, write the shadow price into `phase_12_postimda.md` | Phase 12 post-IMDA    | Decision 4 of 5 (re-solve half). F3.3 is the trap — verify `feasibility: true` directly. |

---

## Sprint 4 — MLOps · Monitor

One phase, three rules; nothing else.

| #   | Decision                                                                                                                                                  | Owning phase | Notes                                                       |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | ----------------------------------------------------------- |
| M1  | ★ Image retrain rule — signal, threshold, duration window, HITL disposition, seasonal exclusions                                                          | Phase 13     | Decision 5 of 5 (image). Cadence is **weekly** (A7).        |
| M2  | ★ Text retrain rule — signal, threshold, duration window, HITL disposition, seasonal exclusions                                                           | Phase 13     | Decision 5 of 5 (text). Cadence is **daily** (A7).          |
| M3  | ★ Fusion retrain rule — signal, threshold, duration window, HITL disposition, seasonal exclusions                                                         | Phase 13     | Decision 5 of 5 (fusion). Cadence is **per-incident** (A7). |
| M4  | Calibration-decay validity disposition — when the decay signal is identically zero on `recent_30d` (F4.1), which window is the canonical retrain trigger? | Phase 13     | The drift-route does not enforce this; rule body must.      |

---

## Close

| #   | Decision                                                                                           | Owning phase | Notes                                                          |
| --- | -------------------------------------------------------------------------------------------------- | ------------ | -------------------------------------------------------------- |
| Z1  | Cross-sprint red-team findings — severity-ranked, blast-radius in $, detection cadence, mitigation | `/redteam`   | Output: `04-validate/redteam.md`.                              |
| Z2  | Phase 9 codify lessons — 3 transferable + 2 domain-specific                                        | `/codify`    | Anti-platitude check; each lesson must name a Week 7 scenario. |

---

## Summary

- **23 open decisions.** 14 require values you pre-register in a journal; 5 are framing decisions (Phases 1–3); 4 are gate decisions (Phase 8 × 2, Phase 12 × 2 first-pass + post-IMDA).
- **5 ★ decision moments.** All non-negotiable; rubric scores zero on D3 if any are skipped.
- **Replay phases.** Phase 4–8 run twice (Vision then Text); Phase 11–12 run twice (first-pass then post-IMDA). Total 14+5+2+2 = ~22 phase passes excluding `/redteam` + `/codify` + `/wrapup`.

Stopping for `/todos`.
