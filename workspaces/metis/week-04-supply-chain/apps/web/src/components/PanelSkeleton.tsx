"use client";

import type { ReactNode } from "react";

import { cn } from "@/lib/cn";

/**
 * Shared skeleton container for the four data panels that shard 05b will
 * implement (Leaderboard, Forecast, Route, Drift, Journal).
 *
 * Every skeleton carries a visible banner that reads:
 *     # TODO-STUDENT: commissioned live by COC
 *
 * This is a zero-tolerance Rule 2 compliant placeholder — the banner makes
 * it impossible to ship the scaffold with an empty panel masquerading as
 * a working feature.
 */
export interface PanelSkeletonProps {
  title: string;
  /** Plain-language description for non-technical readers (MBA-readable). */
  blurb?: string;
  /** Which data file(s) the panel will eventually read. Displayed in the skeleton. */
  reads?: string[];
  /** Optional footer (empty-state message). */
  children?: ReactNode;
  className?: string;
}

export function PanelSkeleton({
  title,
  blurb,
  reads,
  children,
  className,
}: PanelSkeletonProps) {
  return (
    <section
      className={cn(
        "flex h-full flex-col rounded-lg border border-amber-300 bg-white shadow-sm",
        className,
      )}
      aria-label={`${title} (scaffold pending)`}
    >
      {/* Visible zero-tolerance banner — fades when shard 05b ships. */}
      <div
        role="note"
        className="flex items-center gap-2 rounded-t-lg border-b border-amber-300 bg-amber-100 px-3 py-1.5 text-xs font-semibold text-amber-900"
      >
        <span aria-hidden="true">⚠</span>
        <code className="font-mono">
          # TODO-STUDENT: commissioned live by COC
        </code>
      </div>

      <header className="border-b border-slate-200 px-4 py-3">
        <h2 className="text-base font-semibold text-slate-900">{title}</h2>
        {blurb ? (
          <p className="mt-0.5 text-xs text-slate-600">{blurb}</p>
        ) : null}
      </header>

      <div className="flex-1 space-y-3 px-4 py-4">
        {/* Three rows of stripe-animation skeleton bars. */}
        <div className="h-3 w-3/4 animate-pulse rounded bg-slate-200" />
        <div className="h-3 w-full animate-pulse rounded bg-slate-200" />
        <div className="h-3 w-5/6 animate-pulse rounded bg-slate-200" />
        <div className="h-24 animate-pulse rounded bg-slate-100" />

        {reads && reads.length > 0 ? (
          <p className="pt-2 text-[11px] text-slate-500">
            Will read:{" "}
            {reads.map((r, i) => (
              <span key={r}>
                <code className="rounded bg-slate-100 px-1 py-0.5 font-mono">
                  {r}
                </code>
                {i < reads.length - 1 ? ", " : ""}
              </span>
            ))}
          </p>
        ) : null}

        {children}
      </div>
    </section>
  );
}
