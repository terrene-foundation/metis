<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 9 — Codify

> **What this phase does:** Separates transferable ML-orchestration lessons from Week-5-specific ones, so the course compounds across weeks.
> **Why it exists:** Without deliberate codification, each week's near-misses evaporate and Week 6 students repeat them.
> **You're here because:** You're exploring the Playbook phase inventory. To actually RUN Phase 9 Codify, open `workflow-08-codify.md` at workshop close.

## When this phase runs

Phase 9 Codify does NOT have its own slot in tonight's chronological run order. It runs as part of `workflow-08-codify.md` at workshop close, after `/redteam` completes. The codification work — extracting 3 transferable + 2 domain-specific lessons with cited near-misses — is the Phase 9 content.

## What you do in Phase 9

The core discipline is a deliberate split between what you learned that would apply to any ML product (a forecaster, a recommender, a classifier, an allocator in a different domain) and what you learned that only applies because this is a retail segmentation and optimisation problem. Five lessons total: three transferable, two domain-specific. Each lesson must name the near-miss it prevents — "data quality matters" is a platitude; "AutoML trials above 10 blow the Sprint-1 budget and add no discovery value, confirmed by the Phase 4 sweep results" is a lesson.

The transferable lessons go to the Playbook appendix or to `.claude/skills/project/week-05-lessons.md` so Week 6 students inherit them. The domain-specific lessons go to the domain folder only — they should not pollute lessons that won't transfer. The best lessons are things you almost got wrong tonight, not things that went smoothly. If every lesson is "X went well," the codify produced retrospective praise, not institutional knowledge.

The journal file for this phase is `journal/phase_9_codify.md`. Each lesson entry has a one-line description and a near-miss sentence ("the failure mode this prevents is \_\_\_\_"). Transferable lessons are flagged for appendix export; domain-specific ones are flagged as local-only. The workflow file drives the full prompt and the COC `/codify` workflow step in parallel.

## To run Phase 9 tonight

Open: [`workflow-08-codify.md`](./workflow-08-codify.md)

That file has the paste prompt and the 6-section scaffolding. Return here only if you want background on what Phase 9 is doing and why the transferable/domain split exists.
