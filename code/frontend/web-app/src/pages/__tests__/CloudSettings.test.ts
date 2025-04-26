// ─ src/pages/__tests__/CloudSettings.test.ts ─
import { mount, MountingOptions } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import CloudSettings from '../CloudSettings.vue'
import axios from 'axios'
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
  return mount(CloudSettings, {
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

describe('CloudSettings.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    vi.resetAllMocks()
    wrapper = factory()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the title and subtitle', () => {
    expect(wrapper.text()).toContain('Cloud Settings')
    expect(wrapper.text()).toContain('Configure cloud settings for anomaly detection.')
  })

  it('renders EC2 instance select input with correct default', () => {
    expect((wrapper.vm as any).ec2Instance).toBe('t2.micro')
  })

  it('renders cloud endpoint input with correct default', () => {
    expect((wrapper.vm as any).cloudEndpointUrl).toBe('https://api.cloudprovider.com/v1/upload')
  })

  it('renders timing options with "shift-based" selected', () => {
    expect((wrapper.vm as any).timingsType).toBe('shift-based')
  })

  it('shows start and end time inputs when "shift-based" is selected', () => {
    expect(wrapper.text()).toContain('Start time')
    expect(wrapper.text()).toContain('End time')
    expect((wrapper.vm as any).startTime).toBe('09:00')
    expect((wrapper.vm as any).endTime).toBe('17:00')
  })

  it('renders API key input with correct default', () => {
    expect((wrapper.vm as any).apiKey).toBe('ABCD1234XYZ5678')
  })

  it('renders data usage value', () => {
    expect(wrapper.text()).toContain('0 GB')
  })

  it('renders the retention policy buttons', () => {
    expect(wrapper.text()).toContain('7 days')
    expect(wrapper.text()).toContain('30 days')
    expect(wrapper.text()).toContain('90 days')
    expect((wrapper.vm as any).retentionPolicy).toBe('7days')
  })

  it('handles form submission and logs correct values', async () => {
    const logSpy = vi.spyOn(console, 'log')

    await wrapper.find('form').trigger('submit.prevent')

    expect(logSpy).toHaveBeenCalledWith('EC2 Instance:', 't2.micro')
    expect(logSpy).toHaveBeenCalledWith('Cloud Endpoint URL:', 'https://api.cloudprovider.com/v1/upload')
    expect(logSpy).toHaveBeenCalledWith('Timings Type:', 'shift-based')
    expect(logSpy).toHaveBeenCalledWith('Start Time:', '09:00')
    expect(logSpy).toHaveBeenCalledWith('End Time:', '17:00')
    expect(logSpy).toHaveBeenCalledWith('API Key:', 'ABCD1234XYZ5678')
    expect(logSpy).toHaveBeenCalledWith('Retention Policy:', '7days')

    logSpy.mockRestore()
  })
})
