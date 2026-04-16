/**
 * Typed fetchers for the Nexus backend.
 *
 * Spec: viewer-pane.md §1.2 — backend port is configurable via the
 * NEXT_PUBLIC_BACKEND_PORT env var; default 8000 (canonical-values.md §7).
 *
 * Per viewer-pane.md §2.1 (no cross-origin) and §1.1 (data flow) the
 * Viewer does NOT read Nexus over HTTP for panel data — that flows
 * through the filesystem watcher at /api/workspace/state. These fetchers
 * exist ONLY for display-only fields (e.g. the Preflight banner's live
 * /health read, which surfaces "backend reachable" vs "backend offline").
 *
 * Every fetch has an AbortController timeout so the Viewer stays responsive
 * when Nexus is offline.
 */

const DEFAULT_BACKEND_PORT = 8000;
const DEFAULT_TIMEOUT_MS = 2000;

function backendBaseUrl(): string {
  // env-models.md: ports/URLs come from env, never hard-coded.
  const raw = process.env.NEXT_PUBLIC_BACKEND_PORT;
  const port = raw && /^\d+$/.test(raw) ? Number(raw) : DEFAULT_BACKEND_PORT;
  return `http://localhost:${port}`;
}

export interface HealthResponse {
  ok: boolean;
  db: boolean;
  feature_store: boolean;
  drift_wiring: boolean;
  registry_runs: number;
}

export interface BackendProbeResult {
  reachable: boolean;
  health?: HealthResponse;
  error?: string;
}

/**
 * Probe the Nexus /health endpoint. Returns a never-throwing result so the
 * Viewer can show "backend offline" gracefully (viewer-pane.md §2 failure
 * mode).
 */
export async function probeBackendHealth(
  timeoutMs: number = DEFAULT_TIMEOUT_MS,
): Promise<BackendProbeResult> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(`${backendBaseUrl()}/health`, {
      signal: controller.signal,
      cache: "no-store",
    });
    if (!res.ok) {
      return { reachable: false, error: `HTTP ${res.status}` };
    }
    const health = (await res.json()) as HealthResponse;
    return { reachable: true, health };
  } catch (err) {
    const message = err instanceof Error ? err.message : "unknown error";
    return { reachable: false, error: message };
  } finally {
    clearTimeout(timer);
  }
}

/** Public for components that display the URL (no live fetching). */
export function getBackendBaseUrl(): string {
  return backendBaseUrl();
}
