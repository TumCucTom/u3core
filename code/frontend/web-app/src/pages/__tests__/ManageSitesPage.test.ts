import { mount, MountingOptions } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import ManageSitesPage from '../ManageSitesPage.vue'
import axios from 'axios'
import { routerKey, routeLocationKey } from 'vue-router'

// mocks & stubs
vi.mock('axios')

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

const factory = (options: MountingOptions<any> = {}) => {
  return mount(ManageSitesPage, {
    shallow: true,
    global: {
      provide: {
        _q_: { notify: notifyMock },
        [routerKey]: { push: pushMock },
        [routeLocationKey]: routeMock,
      },
      stubs: {
        'q-page': { template: '<div><slot /></div>' },
        'q-btn': { template: '<button><slot /></button>' },
        'q-avatar': true,
        'q-table': true,
        'q-input': true,
        'q-dialog': true,
        'q-card': true,
        'q-card-section': true,
        'q-card-actions': true,
        'q-separator': true,
      },
      ...options.global,
    },
    ...options,
  })
}

describe('ManageSitesPage.vue', () => {
  let wrapper: any

  beforeEach(() => {
    vi.resetAllMocks()
    wrapper = factory()
  })

  afterEach(() => {
    wrapper.unmount()
  })

  it('fetches sites on fetchSites call', async () => {
    const mockSites = { sites: [{ id: 1, name: 'Test Site' }] }
    axiosMock.get.mockResolvedValueOnce({ data: mockSites })

    await wrapper.vm.fetchSites()

    expect(axios.get).toHaveBeenCalledWith('http://16.171.224.57:80/sites')
    expect(wrapper.vm.sites).toEqual(mockSites.sites)
  })

  it('saves new site', async () => {
    axiosMock.post.mockResolvedValueOnce({ data: {} })

    wrapper.vm.siteName = 'Test Site'
    wrapper.vm.latitude = '12.3456'
    wrapper.vm.longitude = '65.4321'

    await wrapper.vm.saveSite() // <-- changed from saveNewSite to saveSite

    expect(axios.post).toHaveBeenCalledWith('http://16.171.224.57:80/add-site', {
      name: 'Test Site',
      latitude: '12.3456',
      longitude: '65.4321'
    })
  })

  it('resets form correctly', () => {
    // fill fake data
    wrapper.vm.siteName = 'Old Site'
    wrapper.vm.latitude = '1.23'
    wrapper.vm.longitude = '4.56'
    wrapper.vm.locationZone = 'Zone Z'
    wrapper.vm.description = 'Old description'
    wrapper.vm.newCamera = { name: 'Old Cam', RTSPURL: 'oldurl' }

    wrapper.vm.resetForm()

    expect(wrapper.vm.siteName).toBe('')
    expect(wrapper.vm.latitude).toBe('')
    expect(wrapper.vm.longitude).toBe('')
    expect(wrapper.vm.locationZone).toBe('')
    expect(wrapper.vm.description).toBe('')
    expect(wrapper.vm.newCamera).toEqual({ name: '', RTSPURL: '' })
  })
})
