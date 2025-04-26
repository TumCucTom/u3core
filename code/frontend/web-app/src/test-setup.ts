import { beforeAll } from 'vitest'
import { installQuasarPlugin } from '@quasar/quasar-app-extension-testing-unit-vitest'
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

beforeAll(() => {
  installQuasarPlugin()
})
