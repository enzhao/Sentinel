/// <reference types="vitest" />
import { fileURLToPath, URL } from 'node:url'

import type { Plugin } from 'vite'
import { defineConfig, configDefaults } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

/**
 * Custom plugin to replicate Firebase Hosting's `cleanUrls` behavior for the Vite dev server.
 * This allows internal links in the MkDocs site (e.g., /user_docs/some-page/) to correctly
 * resolve to their corresponding index.html file (/user_docs/some-page/index.html).
 */
function mkdocsCleanUrls(): Plugin {
  return {
    name: 'vite-plugin-mkdocs-clean-urls',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        if (req.url?.startsWith('/user_docs/') && req.url.endsWith('/')) {
          req.url += 'index.html';
        }
        next();
      });
    },
  };
}

// https://vite.dev/config/
export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      '/api': {
        // Target the backend server's origin.
        target: 'http://localhost:8000',
        changeOrigin: true,
        // Rewrite the path to include the API version prefix.
        rewrite: (path) => path.replace(/^\/api/, '/api/v1'),
      },
    },
  },
  plugins: [
    vue(),
    vueDevTools(),
    mkdocsCleanUrls(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '~': fileURLToPath(new URL('.', import.meta.url)) // Alias for the frontend root
    },
  },
  test: {
    environment: 'jsdom',
    exclude: [...configDefaults.exclude, 'e2e/**'],
    root: fileURLToPath(new URL('./', import.meta.url)),
    include: ['tests/**/*.spec.ts'],
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    css: true,
    server: {
      deps: {
        inline: ['vuetify'],
      },
    },
  },
})