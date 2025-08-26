import { fileURLToPath } from 'node:url'
import { mergeConfig, defineConfig, configDefaults } from 'vitest/config'
import viteConfig from './vite.config'

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: 'jsdom',
      exclude: [...configDefaults.exclude, 'e2e/**'],
      root: fileURLToPath(new URL('./', import.meta.url)),
      include: ['tests/unit/**/*.spec.ts'],
      globals: true,
      setupFiles: ['./vitest.setup.ts'],
      css: true,
      server: {
        deps: {
          inline: ['vuetify'],
        },
      },
    },
  }),
)
