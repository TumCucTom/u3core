import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import SitesPage from '../SitesPage.vue'
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
  return mount(SitesPage, {
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

describe('SitesPage.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    vi.resetAllMocks()
    wrapper = factory()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders page title and subtitle', () => {
    expect(wrapper.text()).toContain('Manage Sites')
    expect(wrapper.text()).toContain('Track, manage and forecast your customers and orders.')
  })

  it('renders "+ Add Site" button', () => {
    expect(wrapper.text()).toContain('+ Add Site')
  })

  it('renders dashboard cards', () => {
    expect(wrapper.text()).toContain('Total Sites')
    expect(wrapper.text()).toContain('Operational Cameras')
    expect(wrapper.text()).toContain('All Alerts')
  })

  it('renders recent alerts section with buttons', () => {
    expect(wrapper.text()).toContain('Recent alerts')
    expect(wrapper.text()).toContain('Select dates')
    expect(wrapper.text()).toContain('Apply filter')
  })

  it('renders the table with correct columns', () => {
    const expectedColumns = ['Site name', 'Site Location', 'Camera ID', 'Fault Type', 'Timestamp', 'Resource Link']
    expectedColumns.forEach(col => {
      expect(wrapper.text()).toContain(col)
    })
  })

  it('renders all mock table rows', () => {
    const rows = wrapper.vm.tableEntries
    rows.forEach((row: any) => {
      expect(wrapper.text()).toContain(row.site)
      expect(wrapper.text()).toContain(row.location)
      expect(wrapper.text()).toContain(row.camera)
      expect(wrapper.text()).toContain(row.fault)
      expect(wrapper.text()).toContain(row.timestamp)
    })
  })

  it('renders Video and Image buttons in the resource link column', () => {
    expect(wrapper.text()).toContain('Video')
    expect(wrapper.text()).toContain('Image')
  })

  it('renders pagination controls', () => {
    expect(wrapper.text()).toContain('Previous')
    expect(wrapper.text()).toContain('Next')
    expect(wrapper.text()).toContain('Page 1 of 10')
  })
})
