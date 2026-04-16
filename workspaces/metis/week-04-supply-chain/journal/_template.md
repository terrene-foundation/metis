<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# TODO-STUDENT: this is a scaffold placeholder.

# Your prompt to Claude Code must replace this file with the real

# implementation described in SCAFFOLD_MANIFEST.md and PLAYBOOK.md.

# Do NOT edit manually — prompt Claude Code.

#

# This template is copied by `metis journal add` into

# `journal/phase_<N>_<slug>.md` with the frontmatter auto-populated.

# If you are writing an entry by hand, keep all five `##` headings below

# and only remove the ones the rubric applicability matrix marks as n/a

# for your phase (see specs/rubric.md §1.3).

---

phase: <N>
phase_name: "<filled by CLI>"
sprint: <1|2|3|close>
timestamp: <ISO-8601-with-tz>
experiment_run_ids: []
experiment_run_names: []
model_version_ids: []
scenario_tag: null

---

# Phase <N> — <phase_name>

> Rubric dimensions applied to this phase: <list from specs/rubric.md §1.3 applicability matrix>

## Harm framing

Named cost:
Cost asymmetry (in dollars):

## Metric-cost linkage

Metric:
Reason in dollars:

## Trade-off honesty

Chosen (cite ExperimentTracker run ID):
Sacrificed (quantified):

## Constraint classification

Hard constraint(s) (reason):
Soft constraint(s) (penalty in dollars):

## Reversal condition

Signal:
Threshold:
Duration window:
Human-in-the-loop: yes / no (why):

## Notes

Free-form observations, questions for Claude Code, context the grader does not see.
