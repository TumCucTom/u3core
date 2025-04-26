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
const factory = (options:MountingOptions<any> = {}) => {
  return mount(ManageModelsPage, {
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
    expect(wrapper.text()).toContain('+ Add Model')
  })

  it('renders filter buttons', () => {
    const wrapper = factory()
    expect(wrapper.text()).toContain('All')
    expect(wrapper.text()).toContain('Active')
    expect(wrapper.text()).toContain('Paused')
    expect(wrapper.text()).toContain('Completed')
  })

  it('renders search input', () => {
    const wrapper = factory()
    expect(wrapper.text()).toContain('Search')
  })

  it('renders the table with no data message', () => {
    const wrapper = factory()
    const table = wrapper.findComponent({ name: 'q-table' })
    expect(table.exists()).toBe(true)
    expect(wrapper.text()).toContain('No models available yet')
  })

  it('renders pagination controls', () => {
    const wrapper = factory()
    expect(wrapper.text()).toContain('Previous')
    expect(wrapper.text()).toContain('Next')
    expect(wrapper.text()).toContain('Page 1 of 10')
  })
})
