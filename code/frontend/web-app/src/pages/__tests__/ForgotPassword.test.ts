// ─ src/pages/__tests__/ForgotPassword.test.ts ─
import { mount, MountingOptions } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import ForgotPassword from '../ForgotPassword.vue'
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
  return mount(ForgotPassword, {
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

describe('ForgotPassword.vue', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders headings and instructions', () => {
    const wrapper = factory()

    expect(wrapper.text()).toContain('EMAIL VERIFICATION')
    expect(wrapper.text()).toContain('Instructions to Change Password')
    expect(wrapper.text()).toContain('Verify Your Email')
  })

  it('updates email input via v-model', async () => {
    const wrapper = factory()

    wrapper.vm.email = 'test@example.com'
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.email).toBe('test@example.com')
  })

  it('calls API and shows success notification on button click', async () => {
    axiosMock.post.mockResolvedValue({ data: { success: true } })

    const wrapper = factory()

    wrapper.vm.email = 'test@example.com'
    await wrapper.vm.sendVerificationEmail()

    expect(axios.post).toHaveBeenCalledWith(
      'http://16.171.224.57:80/api/sendEmail',
      { email: 'test@example.com' }
    )
    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: expect.stringContaining('Verification email sent successfully')
    }))
  })

  it('handles API error and shows error notification', async () => {
    axiosMock.post.mockRejectedValue(new Error('API Error'))

    const wrapper = factory()

    wrapper.vm.email = 'test@example.com'
    await wrapper.vm.sendVerificationEmail()

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: expect.stringContaining('Error sending verification email')
    }))
  })
})
