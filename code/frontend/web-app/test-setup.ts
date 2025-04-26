import { beforeEach } from 'vitest';
import { Quasar, Dialog, Notify } from 'quasar';
import { config } from '@vue/test-utils';
import { vi } from 'vitest'

vi.mock('vue-router', () => ({
  useRoute: () => ({
    query: { email: 'test@example.com', token: '12345' }
  }),
  useRouter: () => ({
    push: vi.fn()
  })
}))

vi.mock('quasar', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
    useQuasar: () => ({
      dark: { isActive: false, toggle: vi.fn() },
      notify: vi.fn(),
    }),
  }
})


beforeEach(() => {
  config.global.plugins = [Quasar, Dialog, Notify];
});
