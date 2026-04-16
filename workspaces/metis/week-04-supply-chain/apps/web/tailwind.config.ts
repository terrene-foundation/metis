import type { Config } from "tailwindcss";

// Spec: viewer-pane.md §1 — Tailwind only, NO custom CSS files.
const config: Config = {
  content: [
    "./src/app/**/*.{ts,tsx}",
    "./src/components/**/*.{ts,tsx}",
    "./src/lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Severity palette (spec viewer-pane.md §3.5 + §7 colour-blind safety)
        severity: {
          none: "#16a34a", // green-600
          moderate: "#ea580c", // orange-600
          severe: "#dc2626", // red-600
        },
      },
      fontFamily: {
        sans: ["ui-sans-serif", "system-ui", "-apple-system", "sans-serif"],
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
