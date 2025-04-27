import { mount, MountingOptions } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import ManageSitesPage from '../ManageSitesPage.vue'
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
        // only heavy ones manually if needed
        'q-expansion-item': true,
        'q-item': true,
        'q-item-section': true,
        'q-dialog': true,
        'q-card': true,
        'q-card-section': true,
        'q-card-actions': true
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

  it('renders title and Add Camera button', () => {
    expect(wrapper.text()).toContain('Manage Sites')
    expect(wrapper.text()).toContain('orders')
  })

  it('opens Add Site dialog', async () => {
    expect(wrapper.vm.addSiteDialog).toBe(false)
    await wrapper.vm.openAddSiteDialog()
    expect(wrapper.vm.addSiteDialog).toBe(true)
  })

  it('opens Add RTSP dialog', async () => {
    expect(wrapper.vm.addRTSP).toBe(false)
    await wrapper.vm.openAddRTSP()
    expect(wrapper.vm.addRTSP).toBe(true)
  })

  it('fetches sites on created', async () => {
    const mockSites = { sites: [{ id: 1, name: 'Test Site', cameras: [{ id: 101, name: 'Cam 01' }] }] }
    axiosMock.get.mockResolvedValueOnce({ data: mockSites })

    await wrapper.vm.fetchSites()
    expect(axios.get).toHaveBeenCalledWith('http://16.171.224.57:80/sites')
    expect(wrapper.vm.sites).toEqual(mockSites.sites)
  })

  it('saves new site and closes dialog', async () => {
    axiosMock.post.mockResolvedValueOnce({ data: {} })

    wrapper.vm.newSite = {
      name: 'Test Site',
      latitude: '12.3456',
      longitude: '65.4321'
    }

    await wrapper.vm.saveNewSite()

    expect(axios.post).toHaveBeenCalledWith('http://16.171.224.57:80/add-site', {
      name: 'Test Site',
      latitude: '12.3456',
      longitude: '65.4321'
    })
    expect(wrapper.vm.addSiteDialog).toBe(false)
  })

  it('saves new RTSP camera', async () => {
    axiosMock.post.mockResolvedValueOnce({ data: {} })

    wrapper.vm.newCamera = {
      name: 'New Cam',
      RTSPURL: 'rtsp://example.com/stream'
    }

    await wrapper.vm.saveNewRTSP()

    expect(axios.post).toHaveBeenCalledWith('http://16.171.224.57:80/api/add-camera', {
      name: 'New Cam',
      rtsp_url: 'rtsp://example.com/stream'
    })

    expect(wrapper.vm.videoSrc).toBe('rtsp://example.com/stream')
    expect(wrapper.vm.addRTSP).toBe(false)
  })

  it('resets forms correctly', () => {
    wrapper.vm.newSite = { name: 'Old Site', latitude: '0', longitude: '0' }
    wrapper.vm.newCamera = { name: 'Old Cam', RTSPURL: 'url' }

    wrapper.vm.resetForm()

    expect(wrapper.vm.newSite).toEqual({ name: '', latitude: '', longitude: '' })
    expect(wrapper.vm.newCamera).toEqual({ name: '', RTSPURL: '' })
  })
})
