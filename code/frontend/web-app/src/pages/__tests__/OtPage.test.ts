import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import OtPage from '../OtPage.vue'
import axios from 'axios'

// Mock axios
vi.mock('axios')

// Mock $q.notify
const notifyMock = vi.fn()

// Mock router push
const pushMock = vi.fn()

// Set up sessionStorage mock
beforeEach(() => {
  vi.stubGlobal('sessionStorage', {
    getItem: vi.fn((key) => key === 'emailTransfer' ? 'test@example.com' : null),
    setItem: vi.fn(),
    removeItem: vi.fn()
  })
})

describe('OtPage.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    vi.clearAllMocks()
    wrapper = mount(OtPage, {
      global: {
        mocks: {
          $q: { notify: notifyMock },
          $router: { push: pushMock }
        },
        stubs: ['q-page', 'q-avatar', 'q-btn', 'q-icon'],
      }
    })
  })

  afterEach(() => {
    wrapper.unmount()
  })

  it('renders main text and email placeholder', () => {
    expect(wrapper.text()).toContain('Check your email')
    expect(wrapper.text()).toContain('We sent a verification link to')
    expect(wrapper.find('#retrievedEmail').exists()).toBe(true)
  })

  it('calls sendEmail on mount and updates email text', async () => {
    axios.post.mockResolvedValueOnce({ data: {} })

    // Manually trigger sendEmail because mount already called it
    await wrapper.vm.sendEmail()
    const emailSpan = document.getElementById('retrievedEmail')

    expect(emailSpan?.innerHTML).toBe('test@example.com')
    expect(axios.post).toHaveBeenCalledWith(
      'http://16.171.224.57:0080/api/sendVerifyEmail',
      { email: 'test@example.com' }
    )
  })

  it('resends email and shows success notification', async () => {
    axios.post.mockResolvedValueOnce({ data: {} })

    await wrapper.vm.resendEmail()

    expect(axios.post).toHaveBeenCalledWith(
      'http://16.171.224.57:0080/api/sendVerifyEmail',
      { email: 'test@example.com' }
    )
    expect(notifyMock).toHaveBeenCalledWith(
      expect.objectContaining({
        message: expect.stringContaining('Verification email resent successfully')
      })
    )
  })

  it('shows error notification on resend failure', async () => {
    axios.post.mockRejectedValueOnce(new Error('Network Error'))

    await wrapper.vm.resendEmail()

    expect(notifyMock).toHaveBeenCalledWith(
      expect.objectContaining({
        message: expect.stringContaining('Error resending verification email')
      })
    )
  })

  it('navigates back to login page', async () => {
    await wrapper.vm.backtologin()
    expect(pushMock).toHaveBeenCalledWith('/')
  })
})
