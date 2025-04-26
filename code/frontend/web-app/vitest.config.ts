import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'happy-dom',
    // setupFiles: 'src/test-setup.ts',
    globals: true,
    alias: {
      '@/': new URL('./src/', import.meta.url).pathname,
      'assets/': new URL('./src/assets/', import.meta.url).pathname,
      'components/': new URL('./src/components/', import.meta.url).pathname,
    },
  },
  resolve: {
    alias: {
      '@/': new URL('./src/', import.meta.url).pathname,
      'assets/': new URL('./src/assets/', import.meta.url).pathname,
      'components/': new URL('./src/components/', import.meta.url).pathname,
    },
  },
});
