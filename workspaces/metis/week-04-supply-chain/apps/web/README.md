# Metis Viewer Pane (`apps/web/`)

Read-only Next.js 14 cockpit for the Metis Week 4 supply-chain workshop.
Watches the workspace filesystem and renders five panels — Leaderboard,
Forecast, Route Map, Drift, Journal — plus the 12-chip Playbook progress
strip.

**Shard 05a delivers the shell only.** Panel bodies are scaffolded as
skeletons with a visible `# TODO-STUDENT: commissioned live by COC` banner.
Shard 05b fills them in.

## Why filesystem-watch and not HTTP?

The Viewer's data path is local loopback filesystem, not cross-origin HTTP
to Nexus. This eliminates CORS (`viewer-pane.md` §2.1) and lets the Viewer
keep rendering the last-known state when Nexus is offline. Backend
reachability is shown as a small status dot in the top strip, not as a
blocker.

## Quick start

```bash
cd apps/web
npm install
npm run dev
```

Viewer boots at <http://localhost:3000>. The landing page renders even when
the backend is offline — panels show skeleton state + a "backend offline"
notice in the top strip.

## Environment

Copy `.env.example` → `.env.local` and adjust if the defaults don't match
your setup.

| Variable                   | Default                 | Purpose                                              |
| -------------------------- | ----------------------- | ---------------------------------------------------- |
| `NEXT_PUBLIC_BACKEND_PORT` | `8000`                  | Nexus port shown in the status strip + /health probe |
| `NEXT_PUBLIC_POLL_MS`      | `1000`                  | React Query refetch interval (ms)                    |
| `METIS_WORKSPACE_ROOT`     | `path.resolve('../..')` | Absolute path to the workspace root (watcher)        |

All ports come from env (`rules/env-models.md`); no hard-coded model or
URL strings.

## Architecture at a glance

```
Nexus writes data/*.json  ─┐
                           ├─▶  chokidar watcher (server side, Node runtime)
Student writes journal/*  ─┘              │
                                          ▼
                          GET /api/workspace/state  (ETag + 304)
                                          │
                                          ▼
                         React Query (1s refetch, shared cache)
                                          │
                                          ▼
                    Panels + PlaybookProgress + status strip
```

| Path                                    | Role                                                                          |
| --------------------------------------- | ----------------------------------------------------------------------------- |
| `src/app/layout.tsx`                    | Root layout + React Query provider (via `providers.tsx`)                      |
| `src/app/page.tsx`                      | 5-panel grid + inline Playbook progress header                                |
| `src/app/api/workspace/state/...`       | Server-side chokidar watcher returning `{data, journal, preflight}` with ETag |
| `src/hooks/useFileWatch.ts`             | `useWorkspaceState()` + narrow selectors (`useDataFile`, `useJournalFiles`)   |
| `src/components/PlaybookProgress.tsx`   | 12 phase chips + re-run sub-chips (colour by journal file existence)          |
| `src/components/PanelSkeleton.tsx`      | Shared skeleton with `# TODO-STUDENT` banner                                  |
| `src/components/BackendStatusStrip.tsx` | Watcher + `/health` + preflight summary                                       |
| `src/lib/workspace-state.ts`            | Shared `WorkspaceState` types                                                 |
| `src/lib/playbook.ts`                   | Canonical 12-phase list (Week 4 subset of `playbook-universal.md`)            |
| `src/lib/api.ts`                        | Never-throwing `/health` probe                                                |
| `__tests__/fixtures/`                   | Minimal valid JSON for all five data files + `.preflight.json`                |

## Read-only by contract

`viewer-pane.md` §4: no forms, no mutating buttons. Segmented controls
(scenario toggle, depot tab, journal filter) arrive in shard 05b as pure
view state.

## Smoke test: the watcher actually fires

After `npm run dev`:

```bash
# From the workspace root (the one that contains data/ and journal/):
echo '{"hello":"world"}' > data/_test.json
# Within ~1 second, GET /api/workspace/state reflects the new file.
curl -s http://localhost:3000/api/workspace/state | python -m json.tool
```

## Out of scope for shard 05a (handled by 05b)

- Leaderboard panel body
- Forecast Recharts lines with 80% PI band
- Route map with driver-coloured polylines + constraint highlights
- Drift severity chart + recommendations
- Journal markdown rendering with rubric dots
- Preflight-banner failure-specific messaging

## Related rules

- `rules/zero-tolerance.md` Rule 2 — all placeholders are visibly marked
- `rules/terrene-naming.md` — Trust Plane / Execution Plane capitalization
- `rules/env-models.md` — no hardcoded ports/URLs
- `rules/communication.md` — MBA-readable labels in every tooltip/blurb
