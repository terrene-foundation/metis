<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# The Week 5 Playbook — Navigation

**Version:** 2026-04-23 · **License:** CC BY 4.0

Everything you paste tonight lives in this folder. Open the files in the chronological run order below. Each file is self-contained: paste prompt → signals to check → concept refresher → handoff to the next file.

---

## 0. Two flows

1. **`../START_HERE.md`** — read once before class for the overview (what Week 5 is, the product, the two planes, the hygiene toolkit, the grading rubric). Start by pasting the opening prompt in §9 to boot the environment.
2. **This folder, file-by-file** — after the environment is booted, open `workflow-01-analyze.md` and follow the `**Next file:**` pointer at the bottom of each file. Don't skip.

Deep ML concept reference lives in `appendix/` — use it after class, or whenever the in-file §4 quick reference isn't enough.

---

## 1. Tonight's run order (open these files in order)

The viewer at `http://localhost:3000` auto-refreshes as each phase writes artifacts. Glance at it after every phase; if nothing new rendered, Claude Code described the work instead of running it.

| #   | File                                   | What happens                                                       |
| --- | -------------------------------------- | ------------------------------------------------------------------ |
| 1   | `../START_HERE.md` §9 opening prompt   | Boot the backend, viewer, and preflight                            |
| 2   | `workflow-01-analyze.md`               | Inheritance audit — what the scaffold committed to                 |
| 3   | `workflow-02-todos.md`                 | Tracked plan, one todo per Playbook phase (human gate)             |
| 4   | `workflow-03-sprint-1-usml-boot.md`    | Boot Sprint 1 · USML · Discover                                    |
| 5   | `phase-01-frame.md`                    | Target, population, horizon, cost asymmetry                        |
| 6   | `phase-02-data-audit.md`               | Six-category audit                                                 |
| 7   | `phase-03-features.md`                 | Feature framing — availability, leakage, proxy                     |
| 8   | `phase-04-candidates.md` (USML pass)   | Multi-family clustering sweep                                      |
| 9   | `phase-05-implications.md` (USML)      | Name the segments, declare per-segment action                      |
| 10  | `phase-06-metric-threshold.md` (USML)  | Three pre-registered floors (separation, stability, actionability) |
| 11  | `phase-07-redteam.md` (USML)           | Stability / proxy / operational-collapse sweeps                    |
| 12  | `phase-08-gate.md` (USML gate)         | Deployment gate, PASS/FAIL against floors                          |
| 13  | `workflow-04-sprint-2-sml-boot.md`     | Boot Sprint 2 · SML · Predict                                      |
| 14  | `phase-04-candidates.md` (SML replay)  | Same file — now for churn + conversion classifiers                 |
| 15  | `phase-05-implications.md` (SML)       | Pick the family for each classifier                                |
| 16  | `phase-06-metric-threshold.md` (SML)   | PR curve + cost-based threshold + calibration                      |
| 17  | `phase-07-redteam.md` (SML)            | Classifier-specific red-team sweeps                                |
| 18  | `phase-08-gate.md` (SML gate)          | Deployment gate for both classifiers                               |
| 19  | `workflow-05-sprint-3-opt-boot.md`     | Boot Sprint 3 · Optimization · Decide                              |
| 20  | `phase-10-objective.md`                | Allocator objective weights                                        |
| 21  | `phase-11-constraints.md` (first pass) | Hard vs soft constraints                                           |
| 22  | `phase-12-acceptance.md` (first pass)  | LP solve + feasibility + pathology checks                          |
| 23  | **PDPA injection fires** (~4:30pm)     | Instructor-triggered — Legal flags under-18 browsing               |
| 24  | `phase-11-constraints.md` (re-run)     | Re-classify under-18 as hard with $220/record penalty              |
| 25  | `phase-12-acceptance.md` (re-run)      | Re-solve the LP — the plan MUST change visibly                     |
| 26  | `workflow-06-sprint-4-mlops-boot.md`   | Boot Sprint 4 · MLOps · Monitor                                    |
| 27  | `phase-13-drift.md`                    | Three retrain rules (one per model)                                |
| 28  | `workflow-07-redteam.md`               | Cross-sprint cascade red-team                                      |
| 29  | `workflow-08-codify.md`                | Phase 9 Codify — 3 transferable + 2 domain lessons                 |
| —   | End of workshop                        | `/wrapup` writes `.session-notes`                                  |

**Replays are intentional.** Phase-04 through phase-08 are opened TWICE (once USML in Sprint 1, once SML in Sprint 2). Phase-11 and phase-12 are opened twice (first pass + post-PDPA re-run). Each phase file has branched `§1 Tonight-specific` and `§2 Signals` blocks — follow the one that matches your current pass.

**Phase 9 (Codify) is NOT in the run order as `phase-09-codify.md`.** It runs at close via `workflow-08-codify.md`. The `phase-09-codify.md` file is a pointer that explains this.

**Phase 14 (Fairness) is deferred to Week 7.** `phase-14-fairness.md` is a deferred stub.

---

## 2. File types

- **`workflow-NN-*.md`** (8 files) — boot one COC-level step (analyze, todos, 4 sprint boots, redteam, codify). Sets context for the phase walk that follows.
- **`phase-NN-*.md`** (14 files) — run one Playbook ML decision phase. `phase-09` is a pointer, `phase-14` is a deferred stub; the other 12 are full 6-section files.
- **`appendix/`** (themed by ML lifecycle) — passive reference. Don't open during class unless §4 in-file refresher isn't enough.

Legacy files `appendix-a-lessons.md` and `appendix-b-dashboard.md` remain for transferable-lessons accumulation — they're not part of tonight's run order.

---

## 3. Navigation within every file (workflow + phase)

Each file has exactly six sections:

1. **Paste this into Claude Code** — the prompt, split into "Universal core" (transfers to any ML project) + "Tonight-specific additions" (Week 5 retail hooks)
2. **Signals the output is on track** — ✓ success bullets and ✗ drift bullets, including viewer checks
3. **Things you might not understand in this phase** — scannable list of concepts (5–7 bullets)
4. **Quick reference (30 sec, generic)** — ~80-word distilled entry per concept, with a link to the deeper appendix file
5. **Ask CC, grounded in our project (2 min)** — paste-ready template. Fill in the concept name from §3; CC reads our codebase and explains in plain language grounded in Arcadia state
6. **Gate / next** — checklist of concrete outcomes + bolded `**Next file:**` pointer

When you're lost, scan §3 first. Decide whether a 30-second §4 read fixes it or whether you want CC to go deeper via §5.

---

## 4. Where's the overview? Where's the textbook?

- **Overview of the workshop** — `../START_HERE.md` (what Week 5 is, product cascade, Trust/Execution planes, hygiene toolkit, grading, opening prompt)
- **Deep-dive reference on ML concepts** — `appendix/` (themed by ML lifecycle: 01 framing → 02 data → 03 modeling → 04 evaluation → 05 deployment → 06 monitoring → 07 governance)
- **Plain-language explanation grounded in our project** — paste the §5 template in any phase file

---

## 5. Playbook file inventory

| File                                 | Type     | Runs at step | What it contains                                         |
| ------------------------------------ | -------- | ------------ | -------------------------------------------------------- |
| `workflow-01-analyze.md`             | Workflow | 2            | `/analyze` — inheritance audit                           |
| `workflow-02-todos.md`               | Workflow | 3            | `/todos` — tracked plan + human gate                     |
| `workflow-03-sprint-1-usml-boot.md`  | Workflow | 4            | Sprint 1 boot (USML, clustering)                         |
| `workflow-04-sprint-2-sml-boot.md`   | Workflow | 13           | Sprint 2 boot (SML, churn + conversion)                  |
| `workflow-05-sprint-3-opt-boot.md`   | Workflow | 19           | Sprint 3 boot (LP allocator)                             |
| `workflow-06-sprint-4-mlops-boot.md` | Workflow | 26           | Sprint 4 boot (drift × 3 models)                         |
| `workflow-07-redteam.md`             | Workflow | 28           | `/redteam` — cross-sprint cascade stress                 |
| `workflow-08-codify.md`              | Workflow | 29           | `/codify` — Phase 9 transferable lessons                 |
| `phase-01-frame.md`                  | Phase    | 5            | Target / population / horizon / cost asymmetry           |
| `phase-02-data-audit.md`             | Phase    | 6            | Six-category audit with dispositions                     |
| `phase-03-features.md`               | Phase    | 7            | Feature framing — availability / leakage / proxy         |
| `phase-04-candidates.md`             | Phase    | 8, 14        | Multi-family sweep (USML in S1, SML in S2)               |
| `phase-05-implications.md`           | Phase    | 9, 15        | Pick candidate, name segments (USML) / pick family (SML) |
| `phase-06-metric-threshold.md`       | Phase    | 10, 16       | USML three floors · SML PR-curve + calibration           |
| `phase-07-redteam.md`                | Phase    | 11, 17       | Per-sprint red-team sweeps                               |
| `phase-08-gate.md`                   | Phase    | 12, 18       | Deployment gate (PASS/FAIL, rollback, promotion)         |
| `phase-09-codify.md`                 | Pointer  | —            | Explains that Phase 9 runs via `workflow-08-codify.md`   |
| `phase-10-objective.md`              | Phase    | 20           | LP allocator objective weights + shadow prices           |
| `phase-11-constraints.md`            | Phase    | 21, 24       | Hard vs soft constraints · PDPA re-classification        |
| `phase-12-acceptance.md`             | Phase    | 22, 25       | LP acceptance · PDPA re-solve                            |
| `phase-13-drift.md`                  | Phase    | 27           | Three retrain rules (one per model)                      |
| `phase-14-fairness.md`               | Stub     | —            | Deferred to Week 7                                       |
| `appendix/`                          | Folder   | —            | Deep-dive concept reference, themed by ML lifecycle      |
