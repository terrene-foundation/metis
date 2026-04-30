<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# The Week 6 Playbook — Navigation

**Version:** 2026-04-30 · **License:** CC BY 4.0

Everything you paste tonight lives in this folder. Open the files in the chronological run order below. Each file is self-contained: paste prompt → signals to check → concept refresher → handoff to the next file.

---

## 0. Two flows

1. **`../START_HERE.md`** — read once before class for the overview (what Week 6 is, the moderation product, the two planes, the hygiene toolkit, the grading rubric). Start by pasting the opening prompt in §7 to boot the environment.
2. **This folder, file-by-file** — after the environment is booted, open `workflow-01-analyze.md` and follow the `**Next file:**` pointer at the bottom of each file. Don't skip.

Deep ML concept reference lives in `appendix/` — use it after class, or whenever the in-file §4 quick reference isn't enough.

---

## 1. Tonight's run order (open these files in order)

The viewer at `http://localhost:3000` auto-refreshes as each phase writes artifacts. Glance at it after every phase; if nothing new rendered, Claude Code described the work instead of running it.

| #   | File                                    | What happens                                                      |
| --- | --------------------------------------- | ----------------------------------------------------------------- |
| 1   | `../START_HERE.md` §7 opening prompt    | Boot the backend, viewer, and preflight                           |
| 2   | `workflow-01-analyze.md`                | Inheritance audit — what the scaffold committed to                |
| 3   | `workflow-02-todos.md`                  | Tracked plan, one todo per Playbook phase (human gate)            |
| 4   | `workflow-03-sprint-1-vision-boot.md`   | Boot Sprint 1 · Vision/CNN · See                                  |
| 5   | `phase-01-frame.md`                     | Target, population, horizon, cost asymmetry                       |
| 6   | `phase-02-data-audit.md`                | Six-category audit on labelled posts                              |
| 7   | `phase-03-features.md`                  | Feature framing — image features + augmentations + metadata       |
| 8   | `phase-04-candidates.md` (Vision pass)  | CNN unfreeze-depth sweep                                          |
| 9   | `phase-05-implications.md` (Vision)     | Pick CNN architecture; defend in $                                |
| 10  | `phase-06-metric-threshold.md` (Vision) | Per-class thresholds × 5 (csam_adjacent hard-floor)               |
| 11  | `phase-07-redteam.md` (Vision)          | Adversarial / OOD / demographic-skew                              |
| 12  | `phase-08-gate.md` (Vision gate)        | PASS/FAIL, promote to shadow                                      |
| 13  | `workflow-04-sprint-2-text-boot.md`     | Boot Sprint 2 · Text/Transformer · Read                           |
| 14  | `phase-04-candidates.md` (Text replay)  | Same file — now for BERT / RoBERTa / zero-shot LLM                |
| 15  | `phase-05-implications.md` (Text)       | Pick text family                                                  |
| 16  | `phase-06-metric-threshold.md` (Text)   | Per-class thresholds × 5 + calibration                            |
| 17  | `phase-07-redteam.md` (Text)            | Typos / 5-market OOD / demographic                                |
| 18  | `phase-08-gate.md` (Text gate)          | PASS/FAIL, promote to shadow                                      |
| 19  | `workflow-05-sprint-3-fusion-boot.md`   | Boot Sprint 3 · Fusion + Queue · Decide                           |
| 20  | `phase-10-objective.md`                 | Queue allocator LP objective                                      |
| 21  | `phase-11-constraints.md` (first pass)  | Hard vs soft (csam_adjacent PENDING)                              |
| 22  | `phase-12-acceptance.md` (first pass)   | LP solve + feasibility + pathology checks                         |
| 23  | **IMDA injection fires** (~4:30pm)      | Instructor-triggered — IMDA CSAM mandate clarification            |
| 24  | `phase-11-constraints.md` (re-run)      | Re-classify csam_adjacent as hard at 0.40 + 60s SLA               |
| 25  | `phase-12-acceptance.md` (re-run)       | Re-solve LP — quantify compliance cost in $/day                   |
| 26  | `workflow-06-sprint-4-mlops-boot.md`    | Boot Sprint 4 · MLOps · Monitor                                   |
| 27  | `phase-13-drift.md`                     | Three retrain rules (image weekly / text daily / fusion incident) |
| 28  | `workflow-07-redteam.md`                | Cross-sprint cascade red-team                                     |
| 29  | `workflow-08-codify.md`                 | Phase 9 Codify — 3 transferable + 2 domain lessons                |
| —   | End of workshop                         | `/wrapup` writes `.session-notes`                                 |

**Replays are intentional.** Phase-04 through phase-08 are opened TWICE (once Vision in Sprint 1, once Text in Sprint 2). Phase-11 and phase-12 are opened twice (first pass + post-IMDA re-run). Each phase file has branched `§1 Tonight-specific` and `§2 Signals` blocks — follow the one that matches your current pass.

**Phase 9 (Codify) is NOT in the run order as `phase-09-codify.md`.** It runs at close via `workflow-08-codify.md`. The `phase-09-codify.md` file is a pointer that explains this.

**Phase 14 (Fairness) is deferred to Week 7.** `phase-14-fairness.md` is a deferred stub.

---

## 2. File types

- **`workflow-NN-*.md`** (8 files) — boot one COC-level step (analyze, todos, 4 sprint boots, redteam, codify).
- **`phase-NN-*.md`** (14 files) — run one Playbook ML decision phase. `phase-09` is a pointer, `phase-14` is a deferred stub.
- **`appendix/`** (themed by ML lifecycle) — passive reference. Don't open during class unless §4 in-file refresher isn't enough.

Legacy files `appendix-a-lessons.md` and `appendix-b-dashboard.md` accrete across weeks — they're not part of tonight's run order but `/codify` writes to them at close.

---

## 3. Navigation within every file

Each file has exactly six sections:

1. **Paste this into Claude Code** — Universal core + Tonight-specific additions
2. **Signals the output is on track** — ✓ success bullets and ✗ drift bullets
3. **Things you might not understand in this phase** — 5–7 concept bullets
4. **Quick reference (30 sec, generic)** — distilled per-concept entry with link to appendix
5. **Ask CC, grounded in our project (2 min)** — paste-ready template
6. **Gate / next** — checklist + bolded `**Next file:**` pointer

When you're lost, scan §3 first. Decide whether a 30-second §4 read fixes it or whether you want CC to go deeper via §5.

---

## 4. The five Trust Plane decision moments (rubric anchor)

1. Define what counts as harmful (Phase 1 + 2)
2. Set per-class auto-remove thresholds × 10 (Phase 6 × Vision + Text)
3. Choose fusion architecture (Phase 5 multi-modal pass)
4. Re-classify CSAM-adjacent + re-solve queue when IMDA fires (Phase 11+12 re-run)
5. Set retrain rules × 3 cadences (Phase 13)

All five are non-negotiable. The rubric (see `../START_HERE.md` §5) scores each phase journal on five dimensions; the five decision moments are where those dimensions feel teeth.

---

## 5. Where's the overview? Where's the textbook?

- **Overview of the workshop** — `../START_HERE.md` (what Week 6 is, product cascade, planes, hygiene toolkit, grading, opening prompt)
- **Deep-dive reference on ML concepts** — `appendix/` (themed by ML lifecycle: 01 framing → 02 data → 03 modeling → 04 evaluation → 05 deployment → 06 monitoring → 07 governance)
- **Plain-language explanation grounded in our project** — paste the §5 template in any phase file

---

## 6. Playbook file inventory

| File                                  | Type      | Runs at step | What it contains                                       |
| ------------------------------------- | --------- | ------------ | ------------------------------------------------------ |
| `workflow-01-analyze.md`              | Workflow  | 2            | `/analyze` — inheritance audit                         |
| `workflow-02-todos.md`                | Workflow  | 3            | `/todos` — tracked plan + human gate                   |
| `workflow-03-sprint-1-vision-boot.md` | Workflow  | 4            | Sprint 1 boot (CNN image moderator)                    |
| `workflow-04-sprint-2-text-boot.md`   | Workflow  | 13           | Sprint 2 boot (Transformer text moderator)             |
| `workflow-05-sprint-3-fusion-boot.md` | Workflow  | 19           | Sprint 3 boot (multi-modal + queue allocator)          |
| `workflow-06-sprint-4-mlops-boot.md`  | Workflow  | 26           | Sprint 4 boot (drift × 3 cadences)                     |
| `workflow-07-redteam.md`              | Workflow  | 28           | `/redteam` — cross-sprint cascade stress               |
| `workflow-08-codify.md`               | Workflow  | 29           | `/codify` — Phase 9 transferable lessons               |
| `phase-01-frame.md`                   | Phase     | 5            | Target / population / horizon / cost asymmetry         |
| `phase-02-data-audit.md`              | Phase     | 6            | Six-category audit (label quality, leakage, etc.)      |
| `phase-03-features.md`                | Phase     | 7            | Feature framing for vision (Sprint 1)                  |
| `phase-04-candidates.md`              | Phase     | 8, 14        | Multi-family sweep (Vision in S1, Text in S2)          |
| `phase-05-implications.md`            | Phase     | 9, 15        | Pick architecture, defend in $                         |
| `phase-06-metric-threshold.md`        | Phase     | 10, 16       | Per-class thresholds × 5 + calibration                 |
| `phase-07-redteam.md`                 | Phase     | 11, 17       | Per-sprint adversarial / OOD / demographic sweeps      |
| `phase-08-gate.md`                    | Phase     | 12, 18       | Deployment gate (PASS/FAIL, promote, rollback signal)  |
| `phase-09-codify.md`                  | Pointer   | —            | Explains that Phase 9 runs via `workflow-08-codify.md` |
| `phase-10-objective.md`               | Phase     | 20           | Queue allocator LP objective + weights                 |
| `phase-11-constraints.md`             | Phase     | 21, 24       | Hard vs soft + post-IMDA re-classification             |
| `phase-12-acceptance.md`              | Phase     | 22, 25       | LP acceptance + post-IMDA re-solve + compliance cost   |
| `phase-13-drift.md`                   | Phase     | 27           | Three retrain rules (one per model_id)                 |
| `phase-14-fairness.md`                | Stub      | —            | Deferred to Week 7                                     |
| `appendix/`                           | Folder    | —            | Deep-dive concept reference, themed by ML lifecycle    |
| `appendix-a-lessons.md`               | Accretion | —            | Transferable lessons running across weeks              |
| `appendix-b-dashboard.md`             | Reference | —            | How to build a value-chain dashboard at your next job  |
