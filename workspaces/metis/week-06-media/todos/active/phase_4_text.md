<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 4 — Candidates (Text)

**Sprint:** Sprint 2 · Text/Transformer · Read (replay of Phase 4 against text moderator)
**Playbook phase:** Phase 4 — Candidates
**Trust-plane decision:** Read the 3-family text leaderboard (`fine_tuned_bert` / `fine_tuned_roberta` / `zero_shot_llm`) and frame the evidence each family would need to win — without picking yet (Phase 5 picks).
**Paste prompt:** `playbook/phase-04-candidates.md` §1 (Text branch)
**Evaluation checklist:** `playbook/phase-04-candidates.md` §2
**Endpoints touched:** `GET /moderate/text/leaderboard`; optional `POST /moderate/text/train`.
**Skeleton to copy:** `journal/skeletons/phase_4_candidates.md` → `journal/phase_4_text.md` (re-use skeleton, distinct journal file)
**Acceptance criterion:** `journal/phase_4_text.md` exists, three text families' macro_f1 + per-class P/R/F1 captured from `/leaderboard`, each family has a one-paragraph "when it would win" rationale (cost, retrain cadence, OOD handling on Singlish/Malay/code-mixed) — no winner declared.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted — three rationales, no winner yet)
- [ ] Journal entry quotes per-class numbers from `/moderate/text/leaderboard` response
- [ ] Moved to `todos/completed/` on human approval
