/**
 * Canonical 12-chip Week 4 phase list.
 *
 * Spec: viewer-pane.md §3.1 — Sprint 1 [1,2,4,5,6,7,8], Sprint 2 [10,11,12],
 * Sprint 3 [13], Close [9]. Phase 3 is folded into Phase 2 (playbook-universal
 * .md). Phase 14 is deferred to Week 7 and NOT shown in Week 4.
 *
 * Re-run sub-chips (viewer-pane.md §3.1):
 *   Phase 5 — postdrift
 *   Phase 6 — postdrift
 *   Phase 8 — postunion
 *   Phase 11 — postunion
 *   Phase 12 — postunion
 *
 * Chip colour:
 *   green if `journal/phase_<N>_*.md` exists for the base chip;
 *   sub-chip green if `journal/phase_<N>_<suffix>.md` exists.
 */

export type Sprint = 1 | 2 | 3 | "close";

export interface PhaseChip {
  phase: number;
  label: string;
  sprint: Sprint;
  /** Rerun-variant slug — empty array if no sub-chips. */
  reruns: string[];
}

// Ordering below is the exact sprint order from viewer-pane.md §3.1.
export const WEEK4_PHASES: readonly PhaseChip[] = [
  { phase: 1, label: "Frame", sprint: 1, reruns: [] },
  { phase: 2, label: "Data audit", sprint: 1, reruns: [] },
  { phase: 4, label: "Candidates", sprint: 1, reruns: [] },
  { phase: 5, label: "Implications", sprint: 1, reruns: ["postdrift"] },
  { phase: 6, label: "Metric + threshold", sprint: 1, reruns: ["postdrift"] },
  { phase: 7, label: "Red-team", sprint: 1, reruns: [] },
  { phase: 8, label: "Deployment gate", sprint: 1, reruns: ["postunion"] },
  { phase: 10, label: "Objective", sprint: 2, reruns: [] },
  { phase: 11, label: "Constraints", sprint: 2, reruns: ["postunion"] },
  { phase: 12, label: "Solver acceptance", sprint: 2, reruns: ["postunion"] },
  { phase: 13, label: "Drift triggers", sprint: 3, reruns: [] },
  { phase: 9, label: "Codify", sprint: "close", reruns: [] },
] as const;

/**
 * Determine whether a phase's base chip is "done" — i.e. at least one
 * `journal/phase_<N>_*.md` file exists.
 */
export function phaseHasEntry(journalFiles: string[], phase: number): boolean {
  const prefix = `phase_${phase}_`;
  return journalFiles.some((f) => f.startsWith(prefix) && f.endsWith(".md"));
}

/** Sub-chip is "done" when a suffix-specific file exists. */
export function rerunHasEntry(
  journalFiles: string[],
  phase: number,
  rerun: string,
): boolean {
  const target = `phase_${phase}_${rerun}.md`;
  return journalFiles.includes(target);
}

export function sprintLabel(sprint: Sprint): string {
  if (sprint === "close") return "Close";
  return `Sprint ${sprint}`;
}
