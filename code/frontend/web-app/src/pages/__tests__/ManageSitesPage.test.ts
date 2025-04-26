import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import ManageSitesPage from '../ManageSitesPage.vue'
import axios from 'axios'

vi.mock('axios')

// Mock WebSocket globally
global.WebSocket = vi.fn(() => ({
  send: vi.fn(),
  close: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
}));

describe('ManageSitesPage.vue', () => {
  let wrapper: any

  beforeEach(() => {
    vi.resetAllMocks()
    wrapper = mount(ManageSitesPage, {
      global: {
        stubs: ['q-page', 'q-btn', 'q-list', 'q-expansion-item', 'q-item', 'q-item-section', 'q-input', 'q-dialog', 'q-card', 'q-card-section', 'q-card-actions', 'q-form', 'q-img'],
      }
    })
  })

  afterEach(() => {
    wrapper.unmount()
  })

  it('renders title and Add Camera button', () => {
    expect(wrapper.text()).toContain('Manage Sites')
    expect(wrapper.text()).toContain('+ Add Camera')
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
    axios.get.mockResolvedValueOnce({ data: mockSites })

    await wrapper.vm.fetchSites()
    expect(axios.get).toHaveBeenCalledWith('http://16.171.224.57:0080/sites')
    expect(wrapper.vm.sites).toEqual(mockSites.sites)
  })

  it('saves new site and closes dialog', async () => {
    axios.post.mockResolvedValueOnce({ data: {} })

    wrapper.vm.newSite = {
      name: 'Test Site',
      latitude: '12.3456',
      longitude: '65.4321'
    }

    await wrapper.vm.saveNewSite()

    expect(axios.post).toHaveBeenCalledWith('http://16.171.224.57:0080/add-site', {
      name: 'Test Site',
      latitude: '12.3456',
      longitude: '65.4321'
    })
    expect(wrapper.vm.addSiteDialog).toBe(false)
  })

  it('saves new RTSP camera and starts live stream', async () => {
    axios.post.mockResolvedValueOnce({ data: {} })

    wrapper.vm.newCamera = {
      name: 'New Cam',
      RTSPURL: 'rtsp://example.com/stream'
    }

    const startLiveStreamSpy = vi.spyOn(wrapper.vm, 'startLiveStream')

    await wrapper.vm.saveNewRTSP()

    expect(axios.post).toHaveBeenCalledWith('http://16.171.224.57:0080/api/add-camera', {
      name: 'New Cam',
      rtsp_url: 'rtsp://example.com/stream'
    })

    expect(startLiveStreamSpy).toHaveBeenCalled()
    expect(wrapper.vm.videoSrc).toBe('rtsp://example.com/stream')
    expect(wrapper.vm.addRTSP).toBe(false)
  })

  it('starts live streaming and sets streaming to true', async () => {
    await wrapper.vm.startLiveStream()
    expect(wrapper.vm.streaming).toBe(true)
    expect(wrapper.vm.socket).toBeTruthy()
  })

  it('resets forms correctly', async () => {
    wrapper.vm.newSite = { name: 'Old Site', latitude: '0', longitude: '0' }
    wrapper.vm.newCamera = { name: 'Old Cam', RTSPURL: 'url' }

    wrapper.vm.resetForm()

    expect(wrapper.vm.newSite).toEqual({ name: '', latitude: '', longitude: '' })
    expect(wrapper.vm.newCamera).toEqual({ name: '', RTSPURL: '' })
  })
})
