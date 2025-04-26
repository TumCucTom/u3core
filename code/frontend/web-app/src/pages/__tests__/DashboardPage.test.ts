import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import DashboardPage from '../DashboardPage.vue'
import { nextTick } from 'vue'
import axios from 'axios'

vi.mock('axios')

describe('DashboardPage.vue', () => {
  const mockRoute = {
    query: {
      email: encodeURIComponent('test@example.com'),
    },
  }

  beforeEach(() => {
    // Reset all axios mocks
    vi.resetAllMocks()
    axios.get.mockResolvedValue({ data: 0 })
  })

  it('renders with welcome text and name placeholder', async () => {
    const wrapper = mount(DashboardPage, {
      global: {
        stubs: ['q-page', 'q-btn', 'q-icon', 'q-img', 'q-card', 'q-spinner'],
        mocks: {
          $route: mockRoute,
        },
        provide: {
          route: mockRoute, // needed because the component uses useRoute()
        },
      },
    })

    await nextTick()

    expect(wrapper.text()).toContain('Welcome back')
    expect(wrapper.text()).toContain('Track, manage and forecast your customers and orders.')
  })

  it('fetches user name from email in query', async () => {
    axios.get.mockImplementation((url) => {
      if (url.includes('/api/getName')) {
        return Promise.resolve({ data: 'Alice' })
      }
      return Promise.resolve({ data: 0 })
    })

    const wrapper = mount(DashboardPage, {
      global: {
        stubs: ['q-page', 'q-btn', 'q-icon', 'q-img', 'q-card', 'q-spinner'],
        provide: { route: mockRoute },
      },
    })

    await nextTick()
    await new Promise(resolve => setTimeout(resolve, 0)) // resolve async fetch

    expect(wrapper.vm.name).toBe('Alice')
  })

  it('fetches site, camera, and alert counts', async () => {
    axios.get.mockImplementation((url) => {
      if (url.includes('get-site-count')) return Promise.resolve({ data: 5 })
      if (url.includes('get-camera-count')) return Promise.resolve({ data: 10 })
      if (url.includes('get-hazard-count')) return Promise.resolve({ data: 3 })
      return Promise.resolve({ data: 0 })
    })

    const wrapper = mount(DashboardPage, {
      global: {
        stubs: ['q-page', 'q-btn', 'q-icon', 'q-img', 'q-card', 'q-spinner'],
        provide: { route: mockRoute },
      },
    })

    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.vm.siteCount).toBe(5)
    expect(wrapper.vm.cameraCount).toBe(10)
    expect(wrapper.vm.alertCount).toBe(3)
  })

  it('logs on settings button click', async () => {
    const logSpy = vi.spyOn(console, 'log')
    const wrapper = mount(DashboardPage, {
      global: {
        stubs: ['q-page', 'q-btn', 'q-icon', 'q-img', 'q-card', 'q-spinner'],
        provide: { route: mockRoute },
      },
    })

    const button = wrapper.findComponent({ name: 'q-btn' })
    expect(button.exists()).toBe(true)

    await button.trigger('click')
    expect(logSpy).toHaveBeenCalledWith('Settings button clicked')

    logSpy.mockRestore()
  })
})
