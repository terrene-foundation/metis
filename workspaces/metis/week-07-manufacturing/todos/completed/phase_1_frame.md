<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 1 — Frame

**Sprint:** Sprint 1 · Vision QC · Transfer Learning · See (shared framing — also anchors Sprint 2/3/4)
**Playbook phase:** Phase 1 — Frame
**Trust-plane decision:** Define what counts as "shippable" per defect class tonight (auto-pass / human-review / hard-block) per the 4 vision classes; declare population scope, horizon (80 ms/board edge latency), and cost asymmetry quoted from `PRODUCT_BRIEF.md §2`. Tonight's framing also sets the stakes for the predmaint / RL / agent sprints to come.
**Paste prompt:** `playbook/phase-01-frame.md` §1 (universal core + tonight-specific Week 7 block)
**Evaluation checklist:** `playbook/phase-01-frame.md` §2 (signals of success / drift)
**Endpoints touched:** none — Phase 1 is journal-only (no scaffold writes).
**Skeleton to copy:** `journal/skeletons/phase_1_frame.md` → `journal/phase_1_frame.md`
**Acceptance criterion:** `journal/phase_1_frame.md` exists ≥ 500 bytes (auto-detection threshold), items 1–5 (target / population / horizon / cost terms / throughput ceiling) drafted, key cost lines quoted verbatim from `PRODUCT_BRIEF.md §2` ($4,200 major-defect-shipped, $85 false-scrap, $12,000 unplanned-stop, $1,800 planned-stop, $50,000 equipment damage, $35/min inspector, $0.001 edge-inference per board), WSH $1M ceiling acknowledged separately as hard floor, daily dollar-exposure arithmetic shown for the 12,000 inspection events/day baseline.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted)
- [ ] Journal entry cites dollar figures from `PRODUCT_BRIEF.md §2` / `specs/business-costs.md`
- [ ] Moved to `todos/completed/` on human approval
