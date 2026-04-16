---
shard_id: 05
status: SUPERSEDED
superseded_by: [05a, 05b]
reason: >
  Split per H1/H2 invariant-budget finding (red-team convergence report).
  Original shard had 10 invariants and 600-750 realistic LOC — at the upper
  limit of the autonomous-execution.md budget without an explicit feedback-loop
  justification. 05a owns the Next.js shell, chokidar watcher, React Query
  provider, and PlaybookProgress. 05b owns the 5 panel components, PreflightBanner,
  failure modes, and the 3 render-contract tests. See 05a-viewer-shell.md and
  05b-viewer-panels.md.
---

# Shard 05 — SUPERSEDED

This shard has been split into:

- **05a-viewer-shell.md** — Next.js + Shadcn scaffold, chokidar watcher API route, React Query provider, page.tsx grid layout, PlaybookProgress header strip, test fixtures directory
- **05b-viewer-panels.md** — Leaderboard, ForecastPanel, RoutePanel, DriftPanel, JournalPanel, PreflightBanner, failure-mode handling, 3 render-contract tests (severity enum, preflight field naming, leaderboard empty/populated)

Do not implement from this file.
