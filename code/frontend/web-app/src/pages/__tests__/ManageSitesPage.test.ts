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
const factory = (options:MountingOptions<any> = {}) => {
  return mount(ManageSitesPage, {
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
    axiosMock.get.mockResolvedValueOnce({ data: mockSites })

    await wrapper.vm.fetchSites()
    expect(axios.get).toHaveBeenCalledWith('http://16.171.224.57:0080/sites')
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

    expect(axios.post).toHaveBeenCalledWith('http://16.171.224.57:0080/add-site', {
      name: 'Test Site',
      latitude: '12.3456',
      longitude: '65.4321'
    })
    expect(wrapper.vm.addSiteDialog).toBe(false)
  })

  it('saves new RTSP camera and starts live stream', async () => {
    axiosMock.post.mockResolvedValueOnce({ data: {} })

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
