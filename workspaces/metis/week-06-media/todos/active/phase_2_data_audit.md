<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 2 — Data Audit

**Sprint:** Sprint 1 · Vision/CNN · See (shared audit — covers all four modalities once)
**Playbook phase:** Phase 2 — Data Audit (six-category)
**Trust-plane decision:** Confirm the 80k labelled posts (24k image / 56k text / 8k multi-modal) clear a six-category audit — label noise, proxy/leakage, class imbalance, OOD coverage, demographic skew, scaffold coverage — before any modeling phase fires.
**Paste prompt:** `playbook/phase-02-data-audit.md` §1
**Evaluation checklist:** `playbook/phase-02-data-audit.md` §2
**Endpoints touched:** read-only — `GET /moderate/image/leaderboard`, `GET /moderate/text/leaderboard`, `GET /moderate/fusion/leaderboard` to inspect class base rates from the scaffold's reported `per_class.base_rate`.
**Skeleton to copy:** `journal/skeletons/phase_2_data_audit.md` → `journal/phase_2_data_audit.md`
**Acceptance criterion:** `journal/phase_2_data_audit.md` exists, six audit categories each marked with finding + severity + disposition (accept / mitigate-now / flag-for-Phase-7), per-class base rates cited from `/leaderboard` responses, multi-modal subset (8k) audit row separate from image-only / text-only.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted)
- [ ] Journal entry cites at least one base-rate figure from a live `/leaderboard` response
- [ ] Moved to `todos/completed/` on human approval
