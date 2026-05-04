<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 2 — Data Audit

**Sprint:** Sprint 1 · Vision QC · Transfer Learning · See (shared audit — covers all four modules once)
**Playbook phase:** Phase 2 — Data Audit (six-category)
**Trust-plane decision:** Confirm the 800 labelled PCB images, 432,000 sensor rows, 10,000 RL episodes per policy, and 200 procedural safety images clear a six-category audit — label noise, proxy/leakage, class imbalance, OOD coverage, IPC-A-610 Class-3-vs-Class-2 skew, scaffold coverage gaps — before any modeling phase fires.
**Paste prompt:** `playbook/phase-02-data-audit.md` §1
**Evaluation checklist:** `playbook/phase-02-data-audit.md` §2
**Endpoints touched:** read-only — `GET /inspect/vision/leaderboard`, `GET /predict/maintenance/leaderboard`, `GET /optimize/rl/leaderboard` to inspect class base rates, per-window degenerate flags, and per-policy safety_violation counts from the scaffold's reported metrics.
**Skeleton to copy:** `journal/skeletons/phase_2_data_audit.md` → `journal/phase_2_data_audit.md`
**Acceptance criterion:** `journal/phase_2_data_audit.md` exists ≥ 500 bytes, six audit categories each marked with finding + severity + disposition (accept / mitigate-now / flag-for-Phase-7), per-class base rates cited from `/inspect/vision/leaderboard` response, predmaint label-imbalance row separate (4 of 10 machines fail in 30 days = ~13% positive rate), RL episode count + safety_violation count cited per policy, IPC-A-610 Class-3 (60%) vs Class-2 (40%) skew named.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted)
- [ ] Journal entry cites at least one base-rate figure from a live `/leaderboard` response per module
- [ ] Moved to `todos/completed/` on human approval
