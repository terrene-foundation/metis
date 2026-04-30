<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 6 — Metric + Threshold × 5 text classes (Text)

**Sprint:** Sprint 2 · Text/Transformer · Read
**Playbook phase:** Phase 6 — Metric + Threshold (per-class × 5)
**Trust-plane decision:** Set the auto-remove threshold for each of the 5 text classes — `hate_speech`, `harassment`, `threats`, `self_harm`, `safe`. All cost-balanced under $320/$15 (no IMDA hard floor on text). Declare `self_harm` dual action (warn-and-queue floor below auto-remove — `failure-points.md` F2.1) and the class-priority order at decision time (F2.3 — backend default is `threats`/`self_harm` over others; declare or override). (Decision moment 2 of 5, text half.)
**Paste prompt:** `playbook/phase-06-metric-threshold.md` §1 (Sprint 2 / Text branch)
**Evaluation checklist:** `playbook/phase-06-metric-threshold.md` §2
**Endpoints touched:** `GET /moderate/text/threshold`; `POST /moderate/text/threshold` per class (5 calls); read PR-curve evidence from `GET /moderate/text/leaderboard`.
**Skeleton to copy:** `journal/skeletons/phase_6_metric_threshold.md` → `journal/phase_6_text.md`
**Acceptance criterion:** `journal/phase_6_text.md` shows PR curve at K candidate thresholds for each of 5 classes, cost-balanced minimum computed per class with arithmetic, `self_harm` dual-action declared (warn-and-queue threshold + auto-remove threshold + helpline action), class-priority ordering written, 5 successful `POST /moderate/text/threshold` calls reflected in `text_thresholds.json` and `text_registry.json`.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — 5 thresholds POSTed
- [ ] Journal entry quotes $320 / $15 from `PRODUCT_BRIEF.md §2`
- [ ] `self_harm` dual-action declared and class priority documented
- [ ] Moved to `todos/completed/` on human approval
