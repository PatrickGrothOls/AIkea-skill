/** Scope: Build the standalone AIkea review viewer as portable static files. */

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    chunkSizeWarningLimit: 1500,
  },
});
