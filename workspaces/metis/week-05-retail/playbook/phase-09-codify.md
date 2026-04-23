<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Phase 9 — Codify (Close block)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ USML ✓ ▸ SML ✓ ▸ Opt ✓ ▸ MLOps ✓ ▸ **Codify ◉**
 THIS PHASE:    Close · Phase 9 of 14 — Codify
 LEVERS:        transferable lessons · domain-specific lessons
──────────────────────────────────────────────────────────────────
```

### Concept

Before you close the laptop, separate the lessons that transfer to any future ML product from the lessons that only apply to this domain. Three transferable, two domain-specific. Domain goes in the domain folder; transferable lessons append to the Playbook so future students inherit them.

### Why it matters (SML + USML + Opt + MLOps lenses)

- "Data quality matters" is not a lesson. "AutoML trials above 10 blow the Sprint-1 budget and add no discovery value" IS a lesson.
- Transfer test: would this apply if the product were a forecaster, classifier, recommender, or allocator next week?
- The best lessons are _things you almost got wrong tonight_ — not things that went smoothly.

### Your levers this phase

- **Lever 1 (the big one): separate transferable from domain-specific.** Five lessons total, three transferable + two domain-specific is the Codify budget.
- **Lever 2 (the discipline): name the near-miss.** Every transferable lesson pairs with a sentence that starts "the failure mode this prevents is \_\_\_\_".
- **Lever 3 (the persistence): append to the right place.** Transferable → update the Playbook's appendix OR write to `.claude/skills/project/`. Domain-specific → domain folder only.

### Trust-plane question

What transfers to the next domain?

### Paste this

> The `/codify` COC workflow phase shares this Playbook Phase 9. **Paste the `/codify` prompt from `START_HERE.md` §6.8** — that prompt drives Phase 9 at both the COC-workflow-entry and Playbook-phase-detail levels, so there is nothing additional to paste here. Return to §6.8 when you reach Close.

### Evaluation checklist

- [ ] 3 transferable lessons (domain-agnostic, paradigm-agnostic).
- [ ] 2 domain-specific lessons (retail + USML + recommender + allocator).
- [ ] Each lesson includes the near-miss it prevents.
- [ ] Transferable lessons appended to the Playbook appendix (not just the session journal).

### Journal schema — universal

```
Phase 9 — Codify
Transferable:
1. ____ (near-miss prevented: ____)
2. ____ (near-miss prevented: ____)
3. ____ (near-miss prevented: ____)
Domain-specific:
1. ____
2. ____
```

### Common failure modes

- Codify skipped because time ran out — systemic knowledge capture lost.
- Lessons written as platitudes ("be careful") — no near-miss, no transfer.
- Transferable lessons saved only to the session journal — Week 6 students never see them.

### Artefact

`workspaces/.../journal/phase_9_codify.md` + `.claude/skills/project/week-05-lessons.md` + Playbook appendix update.

### Instructor pause point

- Ask: of the five decision moments tonight, which one felt least confident? That is the transferable lesson.
- Ask: which piece was hard _because retail_, and which was hard _because USML+SML+Opt_? Second transfers; first doesn't.
- Demonstrate: read two students' lesson lists. Interchangeable = both too generic. Sharpen with the class.

### Transfer to your next project

1. What did I almost get wrong tonight, and what signal would tell me I'm about to repeat it on a different product?
2. Of my lessons, which would still be true if the product were a classifier / forecaster / recommender / allocator instead of this week's shape?
3. Have I written the domain-specific ones somewhere a future me or a teammate picking up this domain can find, not buried in a chat log?

---

# SPRINT 2 — SML · Predict · Phases 4–8 (replayed)

**What changes in the replay.** Phases 1–3 are shared — the frame, the data audit, the feature classification all apply across Sprints 1 and 2. You RE-RUN Phases 4–8 for the SML classifiers (churn + conversion), producing `journal/phase_{4..8}_sml.md` alongside Sprint 1's `phase_{4..8}_usml.md`. Two artefacts this sprint: churn classifier + conversion classifier. Same family sweep (LR + RF + GBM) and same levers.

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ USML ✓ ▸ **SML ◉** ▸ Opt ▸ MLOps ▸ Close
 THIS SPRINT:   Predict · Phases 4→8 on churn + conversion
 LEVERS:        ensemble-is-the-king · class imbalance · PR curve · calibration
──────────────────────────────────────────────────────────────────
```

