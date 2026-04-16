import { BackendStatusStrip } from "@/components/BackendStatusStrip";
import { PanelSkeleton } from "@/components/PanelSkeleton";
import { PlaybookProgress } from "@/components/PlaybookProgress";

/**
 * Dashboard landing page — the read-only cockpit.
 *
 * Spec: viewer-pane.md §3 — exactly five panel slots in a fixed grid.
 * Shard 05a ships only the shell (skeletons); shard 05b fills in the
 * Leaderboard / RoutePanel / DriftPanel / JournalPanel / ForecastPanel
 * bodies.
 *
 * Brief note: the brief requested a 3-column landing (context / decision /
 * consequences). The authoritative spec pins 5 panels; per specs-authority
 * rules the spec wins. This page renders the 5-panel grid and surfaces the
 * three-column framing inside each panel's copy (what you see, what you
 * decided, what happened).
 */
export default function DashboardPage() {
  return (
    <main className="flex min-h-screen flex-col">
      <BackendStatusStrip />

      <div className="mx-auto w-full max-w-[1400px] space-y-4 px-4 py-4">
        <header className="space-y-1">
          <h1 className="text-xl font-semibold tracking-tight text-slate-900">
            Metis Supply-Chain Workshop — Week 4
          </h1>
          <p className="text-sm text-slate-600">
            Read-only cockpit. All updates arrive via the filesystem watcher; no
            buttons mutate state. The Trust Plane runs in the backend; the
            Execution Plane renders what it produced.
          </p>
        </header>

        {/* Inline playbook progress strip — the 12-chip header. */}
        <PlaybookProgress />

        {/* 5-panel grid. Grid shape chosen so Leaderboard + Forecast get the
            widest row, Route + Drift sit below, Journal spans full width. */}
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2 xl:grid-cols-3">
          <PanelSkeleton
            title="Leaderboard"
            blurb="Your live AutoML run vs the pre-baked 30-trial benchmark."
            reads={["data/leaderboard.json", "data/leaderboard_prebaked.json"]}
            className="xl:col-span-1"
          />
          <PanelSkeleton
            title="Forecast"
            blurb="Per-depot demand forecasts with 80% prediction intervals."
            reads={["data/forecast_output.json"]}
            className="xl:col-span-1"
          />
          <PanelSkeleton
            title="Route Map"
            blurb="Vehicle routes + SLA violations, toggleable across scenarios."
            reads={[
              "data/route_plan.json",
              "data/route_plan_preunion.json",
              "data/route_plan_postunion.json",
            ]}
            className="xl:col-span-1"
          />
          <PanelSkeleton
            title="Drift"
            blurb="Distribution-shift severity against the training baseline."
            reads={["data/drift_report.json", "data/drift_baseline.json"]}
            className="xl:col-span-1"
          />
          <PanelSkeleton
            title="Journal"
            blurb="Decision entries with rubric scores — the audit trail."
            reads={["journal/*.md", "grade_report.json"]}
            className="lg:col-span-2 xl:col-span-2"
          />
        </div>
      </div>
    </main>
  );
}
