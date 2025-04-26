import { beforeAll } from 'vitest'
import { installQuasarPlugin } from '@quasar/quasar-app-extension-testing-unit-vitest'
import { vi } from 'vitest'
import { defineComponent } from 'vue'

// ✅ Correct Quasar mocking — only ONE vi.mock('quasar')
vi.mock('quasar', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
    useQuasar: () => ({
      dark: { isActive: false, toggle: vi.fn() },
      notify: vi.fn(),
      dialog: { create: vi.fn() },
    }),
    QBtn: defineComponent({ name: 'q-btn', template: '<button><slot /></button>' }),
    QCard: defineComponent({ name: 'q-card', template: '<div><slot /></div>' }),
    QToolbar: defineComponent({ name: 'q-toolbar', template: '<div><slot /></div>' }),
    QToolbarTitle: defineComponent({ name: 'q-toolbar-title', template: '<div><slot /></div>' }),
    QCardSection: defineComponent({ name: 'q-card-section', template: '<div><slot /></div>' }),
    QCardActions: defineComponent({ name: 'q-card-actions', template: '<div><slot /></div>' }),
    QIcon: defineComponent({ name: 'q-icon', template: '<i><slot /></i>' }),
    QTable: defineComponent({ name: 'q-table', template: '<table><slot /></table>' }),
    Ripple: {},  // Mock directives
  }
})

// ✅ vue-router mock (still fine)
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

// ✅ install quasar plugin
beforeAll(() => {
  installQuasarPlugin()
})
