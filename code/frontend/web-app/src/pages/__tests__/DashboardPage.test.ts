import { mount, MountingOptions} from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import DashboardPage from '../DashboardPage.vue'
import { nextTick } from 'vue'
import axios from 'axios'
import { routerKey, routeLocationKey } from 'vue-router'

// mocks & stubs
vi.mock('axios')
vi.mock('bcryptjs')

const axiosMock = axios as unknown as {
  get: ReturnType<typeof vi.fn>,
  post: ReturnType<typeof vi.fn>
}
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
  return mount(DashboardPage, {
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

describe('DashboardPage.vue', () => {
  beforeEach(() => {
    vi.resetAllMocks()
    axiosMock.get.mockResolvedValue({ data: 0 })
  })

  it('renders with welcome text and name placeholder', async () => {
    const wrapper = factory()

    await nextTick()

    expect(wrapper.text()).toContain('Welcome back')
    expect(wrapper.text()).toContain('Track, manage and forecast your customers and orders.')
  })

  it('fetches user name from email in query', async () => {
    axiosMock.get.mockImplementation((url) => {
      if (url.includes('/api/getName')) {
        return Promise.resolve({ data: 'Alice' })
      }
      return Promise.resolve({ data: 0 })
    })

    const wrapper = factory()

    await nextTick()
    await new Promise(resolve => setTimeout(resolve, 0)) // flush pending promises

    expect(wrapper.vm.name).toBe('Alice')
  })

  it('fetches site, camera, and alert counts', async () => {
    axiosMock.get.mockImplementation((url) => {
      if (url.includes('get-site-count')) return Promise.resolve({ data: 5 })
      if (url.includes('get-camera-count')) return Promise.resolve({ data: 10 })
      if (url.includes('get-hazard-count')) return Promise.resolve({ data: 3 })
      return Promise.resolve({ data: 0 })
    })

    const wrapper = factory()

    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.vm.siteCount).toBe(5)
    expect(wrapper.vm.cameraCount).toBe(10)
    expect(wrapper.vm.alertCount).toBe(3)
  })

  it('logs on settings button click', async () => {
    const logSpy = vi.spyOn(console, 'log')
    const wrapper = factory()

    const button = wrapper.findComponent({ name: 'q-btn' })
    expect(button.exists()).toBe(true)

    await button.trigger('click')
    expect(logSpy).toHaveBeenCalledWith('Settings button clicked')

    logSpy.mockRestore()
  })
})
