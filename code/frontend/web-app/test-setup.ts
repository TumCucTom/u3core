import { beforeAll } from 'vitest';
import { Quasar } from 'quasar';
import { config } from '@vue/test-utils';
import { vi } from 'vitest';

// Mock vue-router
vi.mock('vue-router', () => ({
  useRoute: () => ({
    query: { email: 'test@example.com', token: '12345' }
  }),
  useRouter: () => ({
    push: vi.fn()
  })
}));

// Mock useQuasar
vi.mock('quasar', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    useQuasar: () => ({
      dark: { isActive: false, toggle: vi.fn() },
      notify: vi.fn(),
    }),
  };
});

// Install Quasar before all tests
beforeAll(() => {
  config.global.plugins = [Quasar];
});
