"use client";

import { useJournalFiles } from "@/hooks/useFileWatch";
import { cn } from "@/lib/cn";
import {
  WEEK4_PHASES,
  phaseHasEntry,
  rerunHasEntry,
  sprintLabel,
  type Sprint,
} from "@/lib/playbook";

/**
 * Inline header strip showing the 12 Week 4 phase chips in sprint order.
 *
 * Spec: viewer-pane.md §3.1. Colour derives from `journal/phase_*.md`
 * filename existence only — never from file contents. Sub-chips for
 * phases 5/6 (postdrift) and 8/11/12 (postunion) render inline beside
 * their parent chip.
 */
export function PlaybookProgress() {
  const journal = useJournalFiles();

  const bySprint = groupBySprint();

  return (
    <nav
      aria-label="Playbook progress"
      className="flex flex-wrap items-center gap-4 rounded-lg border border-slate-200 bg-white px-4 py-3 shadow-sm"
    >
      {bySprint.map(({ sprint, phases }) => (
        <section
          key={String(sprint)}
          className="flex items-center gap-2"
          aria-label={sprintLabel(sprint)}
        >
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
            {sprintLabel(sprint)}
          </span>
          <div className="flex flex-wrap items-center gap-1.5">
            {phases.map((chip) => {
              const done = phaseHasEntry(journal, chip.phase);
              return (
                <div key={chip.phase} className="flex items-center gap-1">
                  <PhaseChipBadge
                    phase={chip.phase}
                    label={chip.label}
                    done={done}
                  />
                  {chip.reruns.map((suffix) => {
                    const rerunDone = rerunHasEntry(
                      journal,
                      chip.phase,
                      suffix,
                    );
                    return (
                      <RerunSubChip
                        key={`${chip.phase}-${suffix}`}
                        suffix={suffix}
                        done={rerunDone}
                      />
                    );
                  })}
                </div>
              );
            })}
          </div>
        </section>
      ))}
    </nav>
  );
}

function PhaseChipBadge({
  phase,
  label,
  done,
}: {
  phase: number;
  label: string;
  done: boolean;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium transition-colors",
        done
          ? "bg-emerald-100 text-emerald-900 ring-1 ring-inset ring-emerald-600/30"
          : "bg-slate-100 text-slate-600 ring-1 ring-inset ring-slate-400/30",
      )}
      title={done ? `Phase ${phase} — journalled` : `Phase ${phase} — pending`}
    >
      <span aria-hidden="true">{done ? "✓" : "•"}</span>
      <span>
        P{phase} {label}
      </span>
    </span>
  );
}

function RerunSubChip({ suffix, done }: { suffix: string; done: boolean }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider",
        done ? "bg-emerald-600/90 text-white" : "bg-slate-300 text-slate-700",
      )}
      title={`Re-run: ${suffix}`}
    >
      {suffix}
    </span>
  );
}

interface SprintGroup {
  sprint: Sprint;
  phases: (typeof WEEK4_PHASES)[number][];
}

function groupBySprint(): SprintGroup[] {
  const order: Sprint[] = [1, 2, 3, "close"];
  return order.map((sprint) => ({
    sprint,
    phases: WEEK4_PHASES.filter((p) => p.sprint === sprint),
  }));
}
