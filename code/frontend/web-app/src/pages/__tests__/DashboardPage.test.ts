import { flushPromises, mount } from '@vue/test-utils'
import { describe, it, beforeEach, expect, vi } from 'vitest'
import DashboardPage from '../DashboardPage.vue'
import axios from 'axios'
import { routerKey, routeLocationKey } from 'vue-router'

// Mock libraries
vi.mock('axios')
vi.mock('bcryptjs')
vi.mock('chart.js', () => ({
  Chart: vi.fn(() => ({
    destroy: vi.fn(),
    update: vi.fn(),
  }))
}))
vi.stubGlobal('HTMLCanvasElement', class {
  getContext() {
    return {}; // return empty object so Chart.js won't crash
  }
});


// Type axios mock
const axiosMock = axios as unknown as {
  get: ReturnType<typeof vi.fn>
  post: ReturnType<typeof vi.fn>
}

// Factory to mount DashboardPage
const factory = () => {
  return mount(DashboardPage, {
    global: {
      provide: {
        _q_: { notify: vi.fn() },
        [routerKey]: { push: vi.fn() },
        [routeLocationKey]: { query: { email: 'test@example.com' } },
      },
      stubs: {
        'q-btn': { template: '<button @click="$emit(\'click\')"><slot /></button>' },
        'q-icon': true,
        'q-card': true,
        'q-img': true,
        'q-page': { template: '<div><slot /></div>' },
        'q-spinner': true,
      },
    }
  })
}

describe('DashboardPage.vue', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('renders welcome text, subtitle, and user name', async () => {
    axiosMock.get.mockResolvedValueOnce({ data: 'Alice' }) // Mock API call for name
    const wrapper = factory()

    await flushPromises()

    expect(wrapper.text()).toContain('Welcome back')
    expect(wrapper.text()).toContain('Track, manage and forecast your asset performance')
    expect(wrapper.text()).toContain('Alice')
  })
})
