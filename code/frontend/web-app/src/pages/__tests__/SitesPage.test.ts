import { mount, MountingOptions } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import SitesPage from '../SitesPage.vue'

// mocks & stubs
vi.mock('axios')
vi.mock('bcryptjs')

// Centralized factory
const factory = (options: MountingOptions<any> = {}) => {
  return mount(SitesPage, {
    global: {
      stubs: {
        'q-page': { template: '<div><slot /></div>' },
        'q-btn': { template: '<button><slot /></button>' },
        'q-card': { template: '<div><slot /></div>' },
        'q-checkbox': { template: '<input type="checkbox" />' },
        'q-table': { template: '<table><slot /></table>' },
      },
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
    const rows = (wrapper.vm as any).tableEntries
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
