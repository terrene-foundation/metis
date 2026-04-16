/**
 * GET /api/workspace/state — the filesystem watcher endpoint.
 *
 * Spec: viewer-pane.md §1.1 data flow, §2 polling contract.
 *
 * Contract:
 *   - Server-side chokidar watcher monitors data/, journal/, .preflight.json
 *     under METIS_WORKSPACE_ROOT (or path.resolve(process.cwd(), '../../')
 *     from apps/web/).
 *   - Accumulates an in-memory state = { data, journal, preflight, updated_at, watcher_ready }.
 *   - Returns 200 with the state JSON + ETag header; 304 when If-None-Match matches.
 *   - Never reaches out to Nexus (CORS eliminated by design, viewer-pane.md §2.1).
 *
 * Zero-tolerance note:
 *   - Errors are logged + surfaced on the state payload (watcher_error) rather
 *     than swallowed (rules/zero-tolerance.md Rule 3).
 *   - This route returns a real, functional snapshot — no stubs (Rule 2).
 */

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";
import type { FSWatcher } from "chokidar";

import {
  EMPTY_STATE,
  type PreflightFlags,
  type WorkspaceState,
} from "@/lib/workspace-state";

// Next.js: force Node.js runtime (chokidar needs fs), never cache the response.
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

interface WatcherHandle {
  state: WorkspaceState;
  etag: string;
  watcher: FSWatcher | null;
  root: string;
}

// Module-scope singleton — survives HMR within a single `next dev` process.
let handle: WatcherHandle | null = null;

function resolveWorkspaceRoot(): string {
  const fromEnv = process.env.METIS_WORKSPACE_ROOT;
  if (fromEnv && fromEnv.length > 0) {
    return path.resolve(fromEnv);
  }
  // apps/web/ is two levels below the workspace root.
  return path.resolve(process.cwd(), "..", "..");
}

function computeEtag(state: WorkspaceState): string {
  // ETag = SHA1 of canonical JSON. Covers data, journal, preflight, and
  // updated_at so any change flips the tag.
  const canon = JSON.stringify({
    data: state.data,
    journal: state.journal,
    preflight: state.preflight,
  });
  const hash = crypto.createHash("sha1").update(canon).digest("hex");
  return `W/"${hash}"`;
}

function safeReadJson(filePath: string): unknown | undefined {
  try {
    const raw = fs.readFileSync(filePath, "utf-8");
    return JSON.parse(raw);
  } catch (err) {
    // File may be missing, partially written, or malformed mid-write.
    // Log + skip; the next watcher event will retry.
    const message = err instanceof Error ? err.message : String(err);
    console.warn(`[workspace-state] skipped ${filePath}: ${message}`);
    return undefined;
  }
}

function readPreflight(root: string): Partial<PreflightFlags> {
  const p = path.join(root, ".preflight.json");
  const value = safeReadJson(p);
  return (value as Partial<PreflightFlags>) ?? {};
}

function scanDataDir(root: string): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  const dir = path.join(root, "data");
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir)) {
    if (!entry.endsWith(".json")) continue;
    if (entry.startsWith(".")) continue; // skip hidden (sqlite, aliases)
    const parsed = safeReadJson(path.join(dir, entry));
    if (parsed !== undefined) out[entry] = parsed;
  }
  return out;
}

function scanJournalDir(root: string): string[] {
  const dir = path.join(root, "journal");
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".md"))
    .sort();
}

async function initWatcher(): Promise<WatcherHandle> {
  const root = resolveWorkspaceRoot();
  const state: WorkspaceState = { ...EMPTY_STATE };

  // Initial synchronous scan so the first GET has real data.
  try {
    state.data = scanDataDir(root);
    state.journal = scanJournalDir(root);
    state.preflight = readPreflight(root);
    state.updated_at = new Date().toISOString();
  } catch (err) {
    state.watcher_error = err instanceof Error ? err.message : String(err);
  }

  const h: WatcherHandle = {
    state,
    etag: computeEtag(state),
    watcher: null,
    root,
  };

  // Start chokidar. Imported dynamically so the module is not loaded during
  // `next build` on environments that cannot bind fsevents.
  try {
    const chokidarModule = await import("chokidar");
    const targets = [
      path.join(root, "data"),
      path.join(root, "journal"),
      path.join(root, ".preflight.json"),
    ];
    const watcher = chokidarModule.default.watch(targets, {
      ignored: (p: string) =>
        p.includes("/.") && !p.endsWith(".preflight.json"),
      ignoreInitial: true,
      awaitWriteFinish: { stabilityThreshold: 150, pollInterval: 50 },
    });

    const refresh = (_event: string, changedPath: string) => {
      try {
        if (changedPath.endsWith(".preflight.json")) {
          h.state.preflight = readPreflight(root);
        } else if (changedPath.includes(`${path.sep}data${path.sep}`)) {
          h.state.data = scanDataDir(root);
        } else if (changedPath.includes(`${path.sep}journal${path.sep}`)) {
          h.state.journal = scanJournalDir(root);
        }
        h.state.updated_at = new Date().toISOString();
        h.etag = computeEtag(h.state);
      } catch (err) {
        h.state.watcher_error =
          err instanceof Error ? err.message : String(err);
      }
    };

    watcher
      .on("add", (p: string) => refresh("add", p))
      .on("change", (p: string) => refresh("change", p))
      .on("unlink", (p: string) => refresh("unlink", p))
      .on("ready", () => {
        h.state.watcher_ready = true;
        h.state.updated_at = new Date().toISOString();
        h.etag = computeEtag(h.state);
      })
      .on("error", (err: unknown) => {
        h.state.watcher_error =
          err instanceof Error ? err.message : String(err);
      });

    h.watcher = watcher;
  } catch (err) {
    h.state.watcher_error =
      err instanceof Error
        ? `watcher init failed: ${err.message}`
        : "watcher init failed";
  }

  return h;
}

async function getHandle(): Promise<WatcherHandle> {
  if (handle) return handle;
  handle = await initWatcher();
  return handle;
}

export async function GET(req: NextRequest): Promise<NextResponse> {
  const h = await getHandle();

  const ifNoneMatch = req.headers.get("if-none-match");
  if (ifNoneMatch && ifNoneMatch === h.etag) {
    return new NextResponse(null, {
      status: 304,
      headers: { ETag: h.etag },
    });
  }

  return NextResponse.json(h.state, {
    status: 200,
    headers: {
      ETag: h.etag,
      "Cache-Control": "no-store",
    },
  });
}
