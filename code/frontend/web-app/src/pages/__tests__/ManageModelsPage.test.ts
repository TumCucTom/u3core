// ─ src/pages/__tests__/ManageModelsPage.test.ts ─
import { mount, MountingOptions } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import ManageModelsPage from '../ManageModelsPage.vue'
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
  return mount(ManageModelsPage, {
    shallow: true,
    global: {
      provide: {
        _q_: { notify: notifyMock },
        [routerKey]: { push: pushMock },
        [routeLocationKey]: routeMock,
      },
      // only stub heavy components manually if needed (or skip stubs entirely!)
      stubs: {
        'q-table': true,  // table is heavy, so we can stub it
        'q-btn-group': true, // optional
      },
      ...options.global,
    },
    ...options,
  })
}


describe('ManageModelsPage.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    wrapper = factory()
  })
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders page title and subtitle', () => {
    const wrapper = factory()
    expect(wrapper.text()).toContain('Manage Models')
    expect(wrapper.text()).toContain('Track, manage and forecast your models and performance.')
  })

  it('renders "+ Add Model" button', () => {
    const wrapper = factory()
    expect(wrapper.text()).toContain('Model')
  })

  it('renders filter buttons', () => {
    const wrapper = factory()
    expect(wrapper.text()).toContain('Manage')
    expect(wrapper.text()).toContain('Track')
  })

  it('renders pagination controls', () => {
    const wrapper = factory()
    expect(wrapper.text()).toContain('Page 1 of 10')
  })
})
