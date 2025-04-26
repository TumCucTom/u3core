// ─ src/pages/__tests__/ForgotPassword.test.ts ─
import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import ForgotPassword from '../ForgotPassword.vue'
import axios from 'axios'
import { Quasar } from 'quasar'

// mocks
vi.mock('axios')

const notifyMock = vi.fn()

// factory function for mounting with correct global config
const factory = (options = {}) => {
  return mount(ForgotPassword, {
    global: {
      plugins: [Quasar],
      provide: {
        _q_: { notify: notifyMock },
      },
      stubs: [
        'q-toolbar', 'q-toolbar-title', 'q-card', 'q-card-section',
        'q-btn', 'q-icon', 'q-input'
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
    axios.post.mockResolvedValue({ data: { success: true } })

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
    axios.post.mockRejectedValue(new Error('API Error'))

    const wrapper = factory()

    wrapper.vm.email = 'test@example.com'
    await wrapper.vm.sendVerificationEmail()

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: expect.stringContaining('Error sending verification email')
    }))
  })
})
