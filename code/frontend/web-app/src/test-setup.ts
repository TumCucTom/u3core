import { vi } from 'vitest'
import { config } from '@vue/test-utils'
import { Quasar, Dialog, Notify } from 'quasar'
import { createRouter, createMemoryHistory } from 'vue-router'
import routes from '@/router/routes'

// Setup a basic router mock
const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

// Tell Vue Test Utils to globally install Quasar and Router
config.global.plugins = [Quasar, Dialog, Notify, router]

// Mock Quasar components that are not critical (optional)
config.global.stubs = {
  'q-btn': true,
  'q-input': true,
  'q-card': true,
  'q-card-section': true,
  'q-toolbar': true,
  'q-toolbar-title': true,
  'q-icon': true,
  'router-link': true,
}

// You can mock common global properties if needed
config.global.mocks = {
  $q: {
    notify: vi.fn(),
  },
}
