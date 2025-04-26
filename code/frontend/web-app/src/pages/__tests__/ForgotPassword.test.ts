import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import ForgotPassword from '../ForgotPassword.vue'
import axios from 'axios'

vi.mock('axios')

const notifyMock = vi.fn()
const $q = {
  notify: notifyMock
}

describe('ForgotPassword.vue', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('renders headings and instructions', () => {
    const wrapper = mount(ForgotPassword, {
      global: {
        stubs: ['q-toolbar', 'q-toolbar-title', 'q-card', 'q-card-section', 'q-btn', 'q-icon', 'q-input'],
      }
    })

    expect(wrapper.text()).toContain('EMAIL VERIFICATION')
    expect(wrapper.text()).toContain('Instructions to Change Password')
    expect(wrapper.text()).toContain('Verify Your Email')
  })

  it('updates email input via v-model', async () => {
    const wrapper = mount(ForgotPassword, {
      global: {
        stubs: ['q-input'],
      }
    })

    wrapper.vm.email = 'test@example.com'
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.email).toBe('test@example.com')
  })

  it('calls API and shows success notification on button click', async () => {
    axios.post.mockResolvedValue({ data: { success: true } })

    const wrapper = mount(ForgotPassword, {
      global: {
        mocks: {
          $q
        },
        stubs: ['q-input', 'q-btn']
      }
    })

    wrapper.vm.email = 'test@example.com'
    await wrapper.vm.sendVerificationEmail()

    expect(axios.post).toHaveBeenCalledWith(
      'http://16.171.224.57:0080/api/sendEmail',
      { email: 'test@example.com' }
    )
    expect(notifyMock).toHaveBeenCalledWith(
      expect.objectContaining({
        message: expect.stringContaining('Verification email sent successfully')
      })
    )
  })

  it('handles API error and shows error notification', async () => {
    axios.post.mockRejectedValue(new Error('API Error'))

    const wrapper = mount(ForgotPassword, {
      global: {
        mocks: {
          $q
        },
        stubs: ['q-input', 'q-btn']
      }
    })

    wrapper.vm.email = 'test@example.com'
    await wrapper.vm.sendVerificationEmail()

    expect(notifyMock).toHaveBeenCalledWith(
      expect.objectContaining({
        message: expect.stringContaining('Error sending verification email')
      })
    )
  })
})
