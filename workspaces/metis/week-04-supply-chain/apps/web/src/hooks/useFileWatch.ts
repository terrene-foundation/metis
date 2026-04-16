"use client";

import { useQuery, type UseQueryResult } from "@tanstack/react-query";

import type { WorkspaceState } from "@/lib/workspace-state";

/**
 * Poll the server-side filesystem watcher at /api/workspace/state.
 *
 * Spec: viewer-pane.md §2 — refetchInterval ≤ 1s end-to-end; the watcher
 * returns 304 Not Modified when nothing changed. React Query treats 304
 * as a no-op (same cached data), so re-renders only happen on real change.
 *
 * This hook is the ONE polling primitive the Viewer uses. Panels read from
 * its cached result through selectors below — they do NOT each start their
 * own poll.
 */
export function useWorkspaceState(): UseQueryResult<WorkspaceState, Error> {
  return useQuery<WorkspaceState, Error>({
    queryKey: ["workspace-state"],
    queryFn: async ({ signal }) => {
      const res = await fetch("/api/workspace/state", {
        signal,
        cache: "no-store",
      });
      if (res.status === 304) {
        // The server returned 304 because the state hash didn't change.
        // React Query will reuse the previous cached value; throw a sentinel
        // so the library does not overwrite the cache with `undefined`.
        throw new NotModifiedError();
      }
      if (!res.ok) {
        throw new Error(`workspace-state HTTP ${res.status}`);
      }
      return (await res.json()) as WorkspaceState;
    },
    // Swallow the sentinel 304 "error" — it's a cache-hit signal, not a bug.
    retry: (failureCount, error) => {
      if (error instanceof NotModifiedError) return false;
      return failureCount < 1;
    },
  });
}

/**
 * Narrow helper: watch a single file under data/ and return its parsed JSON
 * content. Returns `undefined` until the watcher observes the file.
 *
 * Smoke-test: creating data/_test.json causes this to re-fetch within 1s
 * because the shared `useWorkspaceState` query polls at 1000ms.
 */
export function useDataFile<T = unknown>(filename: string): T | undefined {
  const { data } = useWorkspaceState();
  if (!data) return undefined;
  return data.data[filename] as T | undefined;
}

/** Narrow helper: the journal filename list (not contents). */
export function useJournalFiles(): string[] {
  const { data } = useWorkspaceState();
  return data?.journal ?? [];
}

class NotModifiedError extends Error {
  constructor() {
    super("not modified");
    this.name = "NotModifiedError";
  }
}
