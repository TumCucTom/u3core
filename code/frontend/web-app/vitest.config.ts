import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    setupFiles: ['./test-setup.ts'],
    environment: 'happy-dom',
    globals: true,             // optional: allows "describe", "it" globally
  },
});
