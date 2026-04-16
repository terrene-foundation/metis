/**
 * Shared types for the filesystem-watcher workspace-state payload.
 *
 * Spec: viewer-pane.md §1.1 (data flow) — the server-side watcher
 * accumulates this shape from the three roots:
 *   data/              → JSON files keyed by filename
 *   journal/           → markdown filenames only (contents read on demand)
 *   .preflight.json    → single boolean-flag object
 */

export interface PreflightFlags {
  db: boolean;
  feature_store: boolean;
  drift_wiring: boolean;
  ok: boolean;
  xgb_available: boolean;
  explain_available: boolean;
  ortools_available: boolean;
  pulp_available: boolean;
}

export interface WorkspaceState {
  /** Map of data/*.json filename (without dir prefix) → parsed JSON. */
  data: Record<string, unknown>;
  /** List of journal/*.md filenames (without dir prefix), sorted ascending. */
  journal: string[];
  /** Parsed .preflight.json at the workspace root. Partial if file missing. */
  preflight: Partial<PreflightFlags>;
  /** ISO-8601 timestamp of the most recent watcher-observed change. */
  updated_at: string;
  /** True when the watcher has emitted its initial `ready` event. */
  watcher_ready: boolean;
  /** True when the workspace root could not be resolved. */
  watcher_error?: string;
}

export const EMPTY_STATE: WorkspaceState = {
  data: {},
  journal: [],
  preflight: {},
  updated_at: new Date(0).toISOString(),
  watcher_ready: false,
};
