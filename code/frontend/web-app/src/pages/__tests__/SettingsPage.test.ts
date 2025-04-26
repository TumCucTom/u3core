// src/pages/__tests__/SettingsPage.test.ts
import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import SettingsPage from '../SettingsPage.vue'
import { routerKey, routeLocationKey } from 'vue-router'

// mocks & stubs
vi.mock('axios')
vi.mock('bcryptjs')

const notifyMock = vi.fn()
const pushMock = vi.fn()
const routeMock = {
  query: {
    token: '',
    email: ''
  }
}

// Centralized factory
const factory = (options = {}) => {
  return mount(SettingsPage, {
    global: {
      // PROVIDE what useQuasar() and useRouter() will inject:
      provide: {
        // useQuasar() looks up `_q_`
        _q_: { notify: notifyMock },

        // useRouter() looks up this Symbol key
        [routerKey]: { push: pushMock },
        [routeLocationKey]: routeMock,
      },
      // stub out all <q-*> so Quasar never actually runs
      stubs: [
        'q-page','q-btn','q-input','q-avatar',
        'q-img','q-rating','q-checkbox','q-form'
      ],
      ...options.global,
    },
    ...options,
  })
}

describe('SettingsPage.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    vi.resetAllMocks()
    wrapper = factory()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders main Settings title', () => {
    expect(wrapper.text()).toContain('Settings')
  })

  it('renders all tabs', () => {
    expect(wrapper.text()).toContain('Application Settings')
    expect(wrapper.text()).toContain('Camera Edge & device Management')
    expect(wrapper.text()).toContain('User Roles & Permissions')
    expect(wrapper.text()).toContain('Data Privacy & Compliance')
    expect(wrapper.text()).toContain('Integrations')
    expect(wrapper.text()).toContain('API')
  })

  it('switches tabs correctly', async () => {
    expect(wrapper.vm.currentTab).toBe('application')

    wrapper.vm.currentTab = 'privacy'
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.currentTab).toBe('privacy')
  })

  it('toggles notification settings', async () => {
    expect(wrapper.vm.allEventsPush).toBe(true)

    wrapper.vm.allEventsPush = false
    wrapper.vm.allEventsEmail = false
    wrapper.vm.allEventsSMS = true

    await wrapper.vm.$nextTick()

    expect(wrapper.vm.allEventsPush).toBe(false)
    expect(wrapper.vm.allEventsEmail).toBe(false)
    expect(wrapper.vm.allEventsSMS).toBe(true)
  })

  it('selects different data retention plans', async () => {
    expect(wrapper.vm.dataRetention).toBe('basic')

    wrapper.vm.dataRetention = 'enterprise'
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.dataRetention).toBe('enterprise')
  })

  it('toggles Data Privacy options (At Rest, In Transit, Anonymised Data)', async () => {
    expect(wrapper.vm.dataRest).toBe(false)
    expect(wrapper.vm.dataTransit).toBe(false)
    expect(wrapper.vm.anonymisedData).toBe(false)

    wrapper.vm.dataRest = true
    wrapper.vm.dataTransit = true
    wrapper.vm.anonymisedData = true

    await wrapper.vm.$nextTick()

    expect(wrapper.vm.dataRest).toBe(true)
    expect(wrapper.vm.dataTransit).toBe(true)
    expect(wrapper.vm.anonymisedData).toBe(true)
  })
})
