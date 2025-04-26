import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import ResetPassword from '../ResetPassword.vue'
import axios from 'axios'
import { routerKey } from 'vue-router'

// Mocks
vi.mock('axios')

const notifyMock = vi.fn()
const pushMock = vi.fn()

// Centralized factory
const factory = (options = {}) => {
  return mount(ResetPassword, {
    global: {
      provide: {
        _q_: { notify: notifyMock },
        [routerKey]: { push: pushMock },
      },
      stubs: [
        'q-page', 'q-card', 'q-btn', 'q-input',
        'q-icon', 'q-toolbar', 'q-toolbar-title'
      ],
      ...options.global,
    },
    ...options,
  })
}

describe('ResetPassword.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    vi.resetAllMocks()
    wrapper = factory({
      global: {
        mocks: {
          $route: { query: { token: 'abc123', email: encodeURIComponent('test@example.com') } }
        }
      }
    })
  })

  afterEach(() => {
    wrapper.unmount()
  })

  it('renders main headings and password inputs', () => {
    expect(wrapper.text()).toContain('RESET PASSWORD')
    expect(wrapper.text()).toContain('Password Requirements')
    expect(wrapper.text()).toContain('Enter Your New Password')
  })

  it('toggles password visibility', async () => {
    expect(wrapper.vm.showPassword).toBe(false)
    wrapper.vm.togglePassword()
    expect(wrapper.vm.showPassword).toBe(true)

    expect(wrapper.vm.showConfirmPassword).toBe(false)
    wrapper.vm.toggleConfirmPassword()
    expect(wrapper.vm.showConfirmPassword).toBe(true)
  })

  it('handles successful password reset flow', async () => {
    axios.get.mockResolvedValueOnce({ data: ['test@example.com'] })
    axios.post.mockResolvedValueOnce({ data: { message: 'Password updated successfully' } })

    wrapper.vm.newPassword = 'Password1!'
    wrapper.vm.confirmPassword = 'Password1!'

    await wrapper.vm.resetPassword()

    expect(axios.post).toHaveBeenCalledWith('http://16.171.224.57:0080/api/updatePassword', {
      email: 'test@example.com',
      password: 'Password1!',
      token: 'abc123'
    })

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: 'Password changed successfully'
    }))
    expect(pushMock).toHaveBeenCalledWith('/')
  })

  it('shows error if email is not registered', async () => {
    axios.get.mockResolvedValueOnce({ data: ['someoneelse@example.com'] })

    wrapper.vm.newPassword = 'Password1!'
    wrapper.vm.confirmPassword = 'Password1!'

    await wrapper.vm.resetPassword()

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: 'Email is not registered'
    }))
  })

  it('shows error if passwords do not match', async () => {
    axios.get.mockResolvedValueOnce({ data: ['test@example.com'] })

    wrapper.vm.newPassword = 'Password1!'
    wrapper.vm.confirmPassword = 'WrongPassword'

    await wrapper.vm.resetPassword()

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: 'Passwords do not match or do not meet the requirements'
    }))
  })

  it('shows error if server fails during password reset', async () => {
    axios.get.mockResolvedValueOnce({ data: ['test@example.com'] })
    axios.post.mockRejectedValueOnce(new Error('Server Error'))

    wrapper.vm.newPassword = 'Password1!'
    wrapper.vm.confirmPassword = 'Password1!'

    await wrapper.vm.resetPassword()

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: 'Error resetting password'
    }))
  })
})
