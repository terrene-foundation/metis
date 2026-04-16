/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Viewer is read-only + localhost-only (spec: viewer-pane.md §4)
  // No redirects, no headers, no rewrites to external hosts.
  experimental: {
    // chokidar is used by /api/workspace/state route at runtime (server-only).
    serverComponentsExternalPackages: ["chokidar"],
  },
};

export default nextConfig;
