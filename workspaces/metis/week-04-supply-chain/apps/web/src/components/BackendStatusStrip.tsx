"use client";

import { useQuery } from "@tanstack/react-query";

import { useWorkspaceState } from "@/hooks/useFileWatch";
import { cn } from "@/lib/cn";
import { getBackendBaseUrl, probeBackendHealth } from "@/lib/api";
import type { PreflightFlags } from "@/lib/workspace-state";

/**
 * Top-of-viewport status strip — condenses three signals into a single row:
 *
 *   1. Watcher readiness (from the workspace-state hook).
 *   2. Backend reachability (live /health probe against Nexus).
 *   3. Preflight boolean flags (.preflight.json).
 *
 * Spec: viewer-pane.md §3.7 preflight banner + §2 "backend unreachable"
 * stale-strip. Rendered gracefully when backend is offline — the Viewer
 * stays usable for reading last-known state.
 */
export function BackendStatusStrip() {
  const ws = useWorkspaceState();

  const health = useQuery({
    queryKey: ["backend-health"],
    queryFn: () => probeBackendHealth(),
    refetchInterval: 2000,
    retry: 0,
  });

  const watcherReady = ws.data?.watcher_ready ?? false;
  const watcherError = ws.data?.watcher_error;
  const backendReachable = health.data?.reachable ?? false;
  const preflight = ws.data?.preflight ?? {};

  const preflightFailures = collectPreflightFailures(preflight);

  const level = computeLevel({
    watcherReady,
    watcherError,
    backendReachable,
    preflightFailures,
  });

  return (
    <div
      role="status"
      aria-live="polite"
      className={cn(
        "flex flex-wrap items-center gap-x-4 gap-y-1 border-b px-4 py-1.5 text-xs",
        level === "ok" && "border-emerald-200 bg-emerald-50 text-emerald-900",
        level === "warn" && "border-amber-300 bg-amber-50 text-amber-900",
        level === "error" && "border-red-300 bg-red-50 text-red-900",
      )}
    >
      <StatusDot level={level} />

      <span>
        <span className="font-semibold">Backend:</span>{" "}
        {backendReachable
          ? `reachable at ${getBackendBaseUrl()}`
          : `offline at ${getBackendBaseUrl()} — showing last known state`}
      </span>

      <span>
        <span className="font-semibold">Watcher:</span>{" "}
        {watcherError
          ? `error — ${watcherError}`
          : watcherReady
            ? "live"
            : "warming up"}
      </span>

      <span>
        <span className="font-semibold">Preflight:</span>{" "}
        {preflightFailures.length === 0
          ? "all checks green"
          : `failing — ${preflightFailures.join(", ")}`}
      </span>
    </div>
  );
}

function StatusDot({ level }: { level: "ok" | "warn" | "error" }) {
  return (
    <span
      aria-hidden="true"
      className={cn(
        "inline-block h-2 w-2 rounded-full",
        level === "ok" && "bg-emerald-500",
        level === "warn" && "bg-amber-500",
        level === "error" && "bg-red-500",
      )}
    />
  );
}

function collectPreflightFailures(p: Partial<PreflightFlags>): string[] {
  const keys: (keyof PreflightFlags)[] = [
    "db",
    "feature_store",
    "drift_wiring",
    "ok",
    "xgb_available",
    "explain_available",
    "ortools_available",
    "pulp_available",
  ];
  return keys.filter((k) => p[k] === false);
}

function computeLevel(args: {
  watcherReady: boolean;
  watcherError?: string;
  backendReachable: boolean;
  preflightFailures: string[];
}): "ok" | "warn" | "error" {
  if (args.watcherError) return "error";
  if (!args.backendReachable) return "warn";
  if (args.preflightFailures.length > 0) return "warn";
  if (!args.watcherReady) return "warn";
  return "ok";
}
