---
shard_id: 05a
slug: viewer-shell
title: >
  Scaffold the Next.js 14 + Shadcn app structure, the chokidar-based filesystem
  watcher API route (apps/web/app/api/state/route.ts), React Query provider with
  1 s polling, the main page.tsx grid layout, and the PlaybookProgress inline
  header strip — the structural shell every panel component mounts into.
loc_estimate: 200
invariants:
  - no-cross-origin: Viewer never makes HTTP calls to Nexus; all reads go through GET /api/workspace/state (server-side FS watcher only)
  - poll-interval-1s: React Query refetchInterval is NEXT_PUBLIC_POLL_MS (default 1000); watcher endpoint returns 304 on no-change
  - read-only: zero forms, zero state-mutating buttons; scenario toggle + depot tab + journal filter are pure view state
  - watcher-data-shape: route.ts accumulates state as { data: Record<string, unknown>, journal: string[], preflight: Record<string, bool> }; ETag computed from JSON.stringify; 304 returned when ETag matches
  - package-locked: package.json declares next@14, react@18, @tanstack/react-query, recharts, chokidar, tailwindcss; no custom CSS files
call_graph_hops: 3
depends_on: []
blocks: [05b]
can_build_against: sample fixtures in apps/web/__tests__/fixtures/
specs_consulted:
  - specs/viewer-pane.md §1 (architecture: data flow, chokidar watcher, polling contract)
  - specs/viewer-pane.md §2 (polling contract: 1s + 304)
  - specs/viewer-pane.md §3.1 (PlaybookProgress: inline header strip, 12 phase chips, sprint order, re-run sub-chips for phases 5/6/8/11/12)
  - specs/viewer-pane.md §4 (UX invariants: read-only, localhost-only)
  - specs/viewer-pane.md §5 (component ownership table)
  - specs/scaffold-contract.md §5 (frontend file list, all PRE-BUILT)
acceptance_criteria:
  - apps/web/package.json declares next@14, react@18, @tanstack/react-query, recharts, chokidar, tailwindcss; no custom CSS files
  - apps/web/app/api/state/route.ts starts a chokidar watcher on METIS_WORKSPACE_ROOT env or path.resolve(__dirname, '../../data'); accumulates state { data, journal, preflight }; returns current state snapshot with ETag header; returns 304 on no-change since last poll; watches data/ + journal/ + .preflight.json per viewer-pane.md §1.1
  - apps/web/app/layout.tsx sets up React Query provider with defaultOptions.queries.refetchInterval = Number(process.env.NEXT_PUBLIC_POLL_MS ?? 1000)
  - apps/web/app/page.tsx renders exactly 5 panel slots in fixed grid; inline PlaybookProgress chip strip in header position; 12 chips in sprint order; chip colours driven by journal/phase_*.md filename existence (not file contents); re-run sub-chips for phases 5/6/8/11/12 per viewer-pane.md §3.1; empty panel slots show "loading" state when watcher has not yet delivered data
  - apps/web/__tests__/fixtures/ directory contains minimal valid JSON for each data file (leaderboard.json, forecast_output.json, route_plan.json, drift_report.json, drift_baseline.json) + a sample .preflight.json with all 8 fields
wiring_tests: []
---

# Shard 05a — Viewer Shell

## What

Build the structural Next.js scaffold that all panel components mount into: the package setup, the chokidar FS watcher API route, the React Query provider, the page grid layout, and the PlaybookProgress header strip. No panel component bodies — just the shell, routing, and data-delivery infrastructure.

## Why

Separating the shell from the panel bodies lets shard 05b build against a stable data contract without also solving the watcher setup. The chokidar watcher and ETag 304 logic are the highest-risk pieces of the viewer (CORS elimination, no-backend-dep); they deserve their own shard so they can be tested in isolation before all 5 panels are added.

## Implementation sketch

- `apps/web/package.json` — pin all deps; add `"dev": "next dev"` + `"build": "next build"` scripts
- `apps/web/app/api/state/route.ts` — singleton chokidar watcher initialised on first request; accumulates state object in memory; ETag = SHA1 of JSON.stringify(state); if `If-None-Match` header matches, return 304; otherwise return 200 with state JSON
- `apps/web/app/layout.tsx` — `QueryClientProvider` wrapping `{children}`; `defaultOptions.queries.refetchInterval` from env
- `apps/web/app/page.tsx` — 5-slot grid; inline `<PlaybookProgress />` as header; each slot renders `<Suspense fallback="loading">` + panel placeholder div
- `apps/web/app/components/PlaybookProgress.tsx` — reads `journal` string array from watcher state; derives chip presence from filename patterns; renders 12 chips in sprint order per §3.1
- `apps/web/__tests__/fixtures/` — minimal valid JSON files for tests downstream

## Out of scope

- Panel component bodies (shard 05b)
- Authentication (localhost-only by contract)
- Mobile viewport (not a goal)

## Acceptance

- [ ] apps/web/package.json declares all required deps; no custom CSS files
- [ ] apps/web/app/api/state/route.ts returns state snapshot with ETag; returns 304 on no-change; watches correct paths
- [ ] apps/web/app/layout.tsx sets up React Query provider with refetchInterval from env
- [ ] apps/web/app/page.tsx renders 5-slot grid; PlaybookProgress header strip; 12 chips; correct re-run sub-chips for phases 5/6/8/11/12
- [ ] apps/web/**tests**/fixtures/ contains minimal valid fixture files for all 5 data files + .preflight.json
