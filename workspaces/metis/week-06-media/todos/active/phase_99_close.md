<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Close — `/redteam` + `/codify` + `/wrapup`

**Sprint:** Close (post-Sprint 4)
**Playbook phase:** Not a Playbook phase — covers the routine's closing three steps.
**Trust-plane decision:** Run the cross-sprint cascade red-team, codify three transferable + two domain-specific lessons, write `.session-notes` for next session.
**Paste prompts:**

- Red-team: `playbook/workflow-07-redteam.md` §1 → produces `04-validate/redteam.md`
- Codify: `playbook/workflow-08-codify.md` §1 → produces `journal/phase_9_codify.md` AND appends to `playbook/appendix-a-lessons.md`
- Wrapup: `/wrapup` → writes `.session-notes`

**Evaluation checklist:**

- Red-team: `playbook/workflow-07-redteam.md` §2 (≥ 8 findings, severity-ranked, blast-radius in $)
- Codify: `playbook/workflow-08-codify.md` §2 (anti-platitude check; each lesson names a Week 7 scenario)
- Wrapup: `.session-notes` exists with "Where we are / Read first / In-flight state / Traps / Open questions" sections.

**Endpoints touched:** none — all three steps are journal-only.
**Skeleton to copy:** for codify only — `journal/skeletons/phase_9_codify.md` → `journal/phase_9_codify.md`.
**Acceptance criterion:** `04-validate/redteam.md` exists with ≥ 8 cross-sprint findings; `journal/phase_9_codify.md` exists with 3 transferable + 2 domain-specific lessons; `playbook/appendix-a-lessons.md` has a "Week 6 — Media (MosaicHub)" section appended; `.session-notes` exists.

## Status

- [ ] `/redteam` run — `04-validate/redteam.md` written
- [ ] `/codify` run — `phase_9_codify.md` + `appendix-a-lessons.md` updated
- [ ] `/wrapup` run — `.session-notes` written
- [ ] Moved to `todos/completed/` on human approval
