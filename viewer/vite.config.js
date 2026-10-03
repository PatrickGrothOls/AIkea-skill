/** Scope: Build the standalone AIkea review viewer as portable static files. */

import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    license: { fileName: "THIRD_PARTY_LICENSES.md" },
    chunkSizeWarningLimit: 1500,
    emptyOutDir: true,
    outDir: fileURLToPath(
      new URL("../aikea-review-unit/assets/viewer", import.meta.url),
    ),
  },
});
