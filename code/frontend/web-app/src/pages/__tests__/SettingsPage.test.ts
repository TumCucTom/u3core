// src/pages/__tests__/SettingsPage.test.ts
import { mount, MountingOptions } from '@vue/test-utils'
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
const factory = (options: MountingOptions<any> = {}) => {
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
      stubs: {
        'q-icon': true,
        'q-chip': true,
      },
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
    expect(wrapper.text()).toContain('Camera Edge & device Management')
    expect(wrapper.text()).toContain('User Roles & Permissions')
    expect(wrapper.text()).toContain('Data Privacy & Compliance')
    expect(wrapper.text()).toContain('Integrations')
    expect(wrapper.text()).toContain('API')
  })

  it('switches tabs correctly', async () => {
    expect((wrapper.vm as any).currentTab).toBe('application');

    (wrapper.vm as any).currentTab = 'privacy'
    await (wrapper.vm as any).$nextTick()

    expect((wrapper.vm as any).currentTab).toBe('privacy')
  })

  it('toggles notification settings', async () => {
    expect((wrapper.vm as any).allEventsPush).toBe(true);

    (wrapper.vm as any).allEventsPush = false;
    (wrapper.vm as any).allEventsEmail = false;
    (wrapper.vm as any).allEventsSMS = true

    await (wrapper.vm as any).$nextTick()

    expect((wrapper.vm as any).allEventsPush).toBe(false)
    expect((wrapper.vm as any).allEventsEmail).toBe(false)
    expect((wrapper.vm as any).allEventsSMS).toBe(true)
  })

  it('selects different data retention plans', async () => {
    expect((wrapper.vm as any).dataRetention).toBe('basic');

    (wrapper.vm as any).dataRetention = 'enterprise'
    await (wrapper.vm as any).$nextTick()

    expect((wrapper.vm as any).dataRetention).toBe('enterprise')
  })

  it('toggles Data Privacy options (At Rest, In Transit, Anonymised Data)', async () => {
    expect((wrapper.vm as any).dataRest).toBe(false)
    expect((wrapper.vm as any).dataTransit).toBe(false)
    expect((wrapper.vm as any).anonymisedData).toBe(false);

    (wrapper.vm as any).dataRest = true;
    (wrapper.vm as any).dataTransit = true;
    (wrapper.vm as any).anonymisedData = true

    await (wrapper.vm as any).$nextTick()

    expect((wrapper.vm as any).dataRest).toBe(true)
    expect((wrapper.vm as any).dataTransit).toBe(true)
    expect((wrapper.vm as any).anonymisedData).toBe(true)
  })
})
