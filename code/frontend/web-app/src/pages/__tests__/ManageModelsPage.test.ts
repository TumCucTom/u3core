// ─ src/pages/__tests__/ManageModelsPage.test.ts ─
import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import ManageModelsPage from '../ManageModelsPage.vue'
import { routerKey } from 'vue-router'

// Mock axios
vi.mock('axios')

const notifyMock = vi.fn()
const pushMock = vi.fn()

// Centralized mount factory
const mountPage = (options = {}) => mount(ManageModelsPage, {
  global: {
    provide: {
      _q_: { notify: notifyMock },      // for useQuasar().notify
      [routerKey]: { push: pushMock },   // for useRouter().push
    },
    stubs: [
      'q-page', 'q-btn', 'q-btn-group', 'q-input', 'q-table'
    ],
    ...options.global,
  },
  ...options,
})

describe('ManageModelsPage.vue', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders page title and subtitle', () => {
    const wrapper = mountPage()
    expect(wrapper.text()).toContain('Manage Models')
    expect(wrapper.text()).toContain('Track, manage and forecast your models and performance.')
  })

  it('renders "+ Add Model" button', () => {
    const wrapper = mountPage()
    expect(wrapper.text()).toContain('+ Add Model')
  })

  it('renders filter buttons', () => {
    const wrapper = mountPage()
    expect(wrapper.text()).toContain('All')
    expect(wrapper.text()).toContain('Active')
    expect(wrapper.text()).toContain('Paused')
    expect(wrapper.text()).toContain('Completed')
  })

  it('renders search input', () => {
    const wrapper = mountPage()
    expect(wrapper.text()).toContain('Search')
  })

  it('renders the table with no data message', () => {
    const wrapper = mountPage()
    const table = wrapper.findComponent({ name: 'q-table' })
    expect(table.exists()).toBe(true)
    expect(wrapper.text()).toContain('No models available yet')
  })

  it('renders pagination controls', () => {
    const wrapper = mountPage()
    expect(wrapper.text()).toContain('Previous')
    expect(wrapper.text()).toContain('Next')
    expect(wrapper.text()).toContain('Page 1 of 10')
  })
})
