<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Close — `/redteam` + `/codify` + `/wrapup`

**Sprint:** Close (post-Sprint 4)
**Playbook phase:** Not a Playbook phase — covers the routine's closing three steps.
**Trust-plane decision:** Run the cross-sprint cascade red-team (vision → predmaint → RL → agent → drift), codify three transferable + two domain-specific lessons, write `.session-notes` for the next session.
**Paste prompts:**

- Red-team: `playbook/workflow-07-redteam.md` §1 → produces `04-validate/redteam.md`
- Codify: `playbook/workflow-08-codify.md` §1 → produces `journal/phase_9_codify.md` AND appends to `playbook/appendix-a-lessons.md`
- Wrapup: `/wrapup` → writes `.session-notes`

**Evaluation checklist:**

- Red-team: `playbook/workflow-07-redteam.md` §2 (≥ 8 findings, severity-ranked, blast-radius in $)
- Codify: `playbook/workflow-08-codify.md` §2 (anti-platitude check; each lesson must name a Week 7 scenario)
- Wrapup: `.session-notes` exists with "Where we are / Read first / In-flight state / Traps / Open questions" sections.

**Endpoints touched:** none — all three steps are journal-only.
**Skeleton to copy:** for codify only — `journal/skeletons/phase_99_close.md` → `journal/phase_9_codify.md`.
**Acceptance criterion:** `04-validate/redteam.md` exists with ≥ 8 cross-sprint findings (must include the cascade chain F1.1 → F2.2 → F3.1 → F4.2 OR an equivalent end-to-end thread); `journal/phase_9_codify.md` exists with 3 transferable + 2 domain-specific lessons (transferable: macro-F1 trap, in-sample calibration trap, Goodhart's Law on RL reward; domain-specific: WSH hard floor as structural override, MOM mandate as multi-endpoint hard-shadow); `playbook/appendix-a-lessons.md` has a "Week 7 — Manufacturing (LumenCircuit)" section appended; `.session-notes` exists.

## Status

- [ ] `/redteam` run — `04-validate/redteam.md` written with ≥ 8 findings
- [ ] `/codify` run — `phase_9_codify.md` + `appendix-a-lessons.md` updated
- [ ] `/wrapup` run — `.session-notes` written
- [ ] Moved to `todos/completed/` on human approval
