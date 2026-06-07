/// <reference types="vitest" />

import react from "@vitejs/plugin-react-swc";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "~": `${process.cwd()}/src`,
    },
  },
  server: {
    port: 3000,
  },
  test: {
    css: false,
    environment: "jsdom",
    globals: true,
    setupFiles: "src/tests/setup.ts",
  },
});
