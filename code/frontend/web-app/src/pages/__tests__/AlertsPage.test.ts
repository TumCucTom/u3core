import { mount, MountingOptions } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import AlertsPage from '../AlertsPage.vue'
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
const factory = (options:MountingOptions<any> = {}) => {
  return mount(AlertsPage, {
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

describe('AlertsPage.vue', () => {
  let wrapper: ReturnType<typeof mount>
  beforeEach(() => {
    wrapper = factory()
  })

  afterEach(() => {
    vi.clearAllMocks()
    wrapper.unmount()
  })

  it('renders the page title and subtitle', () => {
    expect(wrapper.text()).toContain('Alerts')
    expect(wrapper.text()).toContain('Track and manage your alerts')
  })

  it('renders the table component', () => {
    const table = wrapper.findComponent({ name: 'q-table' })
    expect(table.exists()).toBe(true)
  })

  it('calls fetchAlerts on mount', async () => {
    const mockData = [
      {
        id: 1,
        cameraName: 'Cam 1',
        cameraAddress: '123 Street',
        timestamp: '2023-01-01 10:00:00',
        faultType: 'Motion',
        numberOfHazards: 5,
        falsePositives: 1,
      },
    ]

    // Mock fetch properly with vi
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      json: () => Promise.resolve(mockData),
    }))

    await (wrapper.vm as any).fetchAlerts()
    await (wrapper.vm as any).$nextTick()

    expect((wrapper.vm as any).alertsData).toEqual(mockData)
    expect(fetch).toHaveBeenCalledTimes(1)

    // Clean up the global stub to not leak into other tests
    vi.unstubAllGlobals()
  })

  it('sets up polling on mount and clears on unmount', async () => {
    const clearIntervalSpy = vi.spyOn(window, 'clearInterval')

    const intervalId = (wrapper.vm as any).pollInterval
    expect(intervalId).toBeTruthy()

    wrapper.unmount()
    expect(clearIntervalSpy).toHaveBeenCalledWith(intervalId)

    clearIntervalSpy.mockRestore()
  })

  it('handles fetch error gracefully', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Network Error')))

    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})

    await (wrapper.vm as any).fetchAlerts()

    expect(consoleErrorSpy).toHaveBeenCalledWith('Error fetching alerts:', expect.any(Error))

    consoleErrorSpy.mockRestore()
    vi.unstubAllGlobals() // Clean up after the test
  })

})
