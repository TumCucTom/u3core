import { config } from '@vue/test-utils'
import { Quasar } from 'quasar'
import { beforeAll } from 'vitest'
import { vi } from 'vitest'

// Correct Quasar mocking
vi.mock('quasar', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
    useQuasar: () => ({
      dark: { isActive: false, toggle: vi.fn() },
      notify: vi.fn(),
      dialog: { create: vi.fn() },
    }),
  }
})

// Mock vue-router
vi.mock('vue-router', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
    useRoute: () => ({
      query: { email: 'test@example.com', token: '12345' },
    }),
    useRouter: () => ({
      push: vi.fn(),
    }),
  }
})

// install Quasar properly
beforeAll(() => {
  config.global.plugins = [[Quasar, {}]]; // with empty options
});
