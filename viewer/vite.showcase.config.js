/** Scope: Build the public showcase independently of the installed skill viewer. */
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

export default defineConfig({
  root: fileURLToPath(new URL("./showcase", import.meta.url)),
  base: "./",
  build: {
    outDir: fileURLToPath(new URL("./showcase-dist", import.meta.url)),
    emptyOutDir: true,
    license: {fileName: "THIRD_PARTY_LICENSES.md"},
    chunkSizeWarningLimit: 800,
  },
});
