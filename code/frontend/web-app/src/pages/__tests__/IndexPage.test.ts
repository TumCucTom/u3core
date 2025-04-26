import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import IndexPage from '../IndexPage.vue'
import axios from 'axios'
import { Quasar } from 'quasar'
import { routerKey } from 'vue-router'

// Mock axios
vi.mock('axios')

// Create centralized factory
const factory = (options = {}) => {
  return mount(IndexPage, {
    global: {
      plugins: [Quasar],
      provide: {
        // Provide dummy Quasar and Router context if needed
        _q_: { notify: vi.fn() },
        [routerKey]: { push: vi.fn() }
      },
      stubs: ['q-page', 'q-btn', 'q-img'],
      ...options.global,
    },
    ...options,
  })
}

describe('IndexPage.vue', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the logo image', () => {
    const wrapper = factory()

    const img = wrapper.find('img')
    expect(img.exists()).toBe(true)
    expect(img.attributes('alt')).toBe('Quasar logo')
  })
})
