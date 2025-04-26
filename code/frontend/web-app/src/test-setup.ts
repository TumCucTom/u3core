import { beforeAll } from 'vitest'
import { installQuasarPlugin } from '@quasar/quasar-app-extension-testing-unit-vitest'
import { vi } from 'vitest'
import { defineComponent } from 'vue'

// Correct hoist-safe Quasar mocking
vi.mock('quasar', () => {
  const actual = vi.importActual<any>('quasar')
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

// Correct hoist-safe vue-router mocking
vi.mock('vue-router', () => {
  const actual = vi.importActual<any>('vue-router')
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

// Install quasar plugin
beforeAll(() => {
  installQuasarPlugin()
})
