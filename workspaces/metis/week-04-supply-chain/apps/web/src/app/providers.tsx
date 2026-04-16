"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState, type ReactNode } from "react";

/**
 * Root client-side providers.
 *
 * Spec: viewer-pane.md §2 — poll at NEXT_PUBLIC_POLL_MS (default 1000ms).
 * Stale state is rendered optimistically; the watcher endpoint returns
 * 304 when nothing changed so the React Query cache stays put.
 */
const DEFAULT_POLL_MS = 1000;

function pollIntervalMs(): number {
  const raw = process.env.NEXT_PUBLIC_POLL_MS;
  if (raw && /^\d+$/.test(raw)) {
    const parsed = Number(raw);
    if (parsed > 0) return parsed;
  }
  return DEFAULT_POLL_MS;
}

export function Providers({ children }: { children: ReactNode }) {
  const [client] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            refetchInterval: pollIntervalMs(),
            refetchOnWindowFocus: false,
            // Keep last-known state visible even on error — viewer-pane.md §2
            // "keeps rendering the last known state with a red strip".
            staleTime: 0,
            gcTime: 5 * 60_000,
            retry: 1,
          },
        },
      }),
  );

  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}
