import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import LoginPage from '../LoginPage.vue'
import axios from 'axios'
import bcrypt from 'bcryptjs'

// Mocks
vi.mock('axios')
vi.mock('bcryptjs', async () => {
  const actual = await vi.importActual<typeof import('bcryptjs')>('bcryptjs')
  return {
    ...actual,
    compare: vi.fn(),
  }
})

const notifyMock = vi.fn()
const pushMock = vi.fn()

const $q = { notify: notifyMock }
const $router = { push: pushMock }

describe('LoginPage.vue', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('renders correctly in signup mode by default', () => {
    const wrapper = mount(LoginPage, {
      global: {
        stubs: ['q-page', 'q-btn', 'q-input', 'q-avatar', 'q-img', 'q-rating', 'q-checkbox', 'q-form'],
      }
    })

    expect(wrapper.vm.isLogin).toBe(false)
    expect(wrapper.text()).toContain('Sign up')
    expect(wrapper.text()).toContain('First Name')
    expect(wrapper.text()).toContain('Last Name')
  })

  it('toggles to login mode', async () => {
    const wrapper = mount(LoginPage, {
      global: {
        stubs: ['q-page', 'q-btn', 'q-input', 'q-avatar', 'q-img', 'q-rating', 'q-checkbox', 'q-form'],
      }
    })

    expect(wrapper.vm.isLogin).toBe(false)
    await wrapper.vm.toggleMode()
    expect(wrapper.vm.isLogin).toBe(true)
    expect(wrapper.text()).toContain('Welcome back')
  })

  it('handles successful signup flow', async () => {
    axios.get.mockResolvedValue({ data: ['existing@example.com'] }) // Emails from server
    axios.post.mockResolvedValue({ data: 'success' })

    const wrapper = mount(LoginPage, {
      global: {
        mocks: { $q },
        stubs: ['q-page', 'q-btn', 'q-input', 'q-avatar', 'q-img', 'q-rating', 'q-checkbox', 'q-form'],
      }
    })

    // Fill form data
    wrapper.vm.email = 'newuser@example.com'
    wrapper.vm.firstName = 'John'
    wrapper.vm.lastName = 'Doe'
    wrapper.vm.password = 'Password1!'

    // Mock that the email does NOT already exist
    axios.get.mockResolvedValueOnce({ data: ['someoneelse@example.com'] })

    await wrapper.vm.onSubmit()

    expect(axios.post).toHaveBeenCalledWith(
      'http://16.171.224.57:0080/api/addToCustomer',
      { items: ['John', 'Doe', 'newuser@example.com', 'Password1!'] }
    )
    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: expect.stringContaining('Email registered')
    }))
  })

  it('handles duplicate email on signup', async () => {
    axios.get.mockResolvedValue({ data: ['test@example.com'] })

    const wrapper = mount(LoginPage, {
      global: {
        mocks: { $q },
        stubs: ['q-page', 'q-btn', 'q-input', 'q-avatar', 'q-img', 'q-rating', 'q-checkbox', 'q-form'],
      }
    })

    wrapper.vm.email = 'test@example.com'
    await wrapper.vm.onSubmit()

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: expect.stringContaining('already registered')
    }))
  })

  it('handles successful login flow', async () => {
    axios.get.mockResolvedValue({ data: '$2a$10$hashedpassword' })
    bcrypt.compare.mockResolvedValue(true)

    const wrapper = mount(LoginPage, {
      global: {
        mocks: { $q, $router },
        stubs: ['q-page', 'q-btn', 'q-input', 'q-avatar', 'q-img', 'q-rating', 'q-checkbox', 'q-form'],
      }
    })

    wrapper.vm.email = 'test@example.com'
    wrapper.vm.password = 'Password1!'
    await wrapper.vm.onLogin()

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: expect.stringContaining('Successfully logged in')
    }))
    expect(pushMock).toHaveBeenCalledWith('/otp')
  })

  it('handles invalid password login flow', async () => {
    axios.get.mockResolvedValue({ data: '$2a$10$hashedpassword' })
    bcrypt.compare.mockResolvedValue(false)

    const wrapper = mount(LoginPage, {
      global: {
        mocks: { $q },
        stubs: ['q-page', 'q-btn', 'q-input', 'q-avatar', 'q-img', 'q-rating', 'q-checkbox', 'q-form'],
      }
    })

    wrapper.vm.email = 'test@example.com'
    wrapper.vm.password = 'wrongpassword'
    await wrapper.vm.onLogin()

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: expect.stringContaining('Invalid username/password')
    }))
  })

  it('handles login error (email not found)', async () => {
    axios.get.mockRejectedValue(new Error('Not Found'))

    const wrapper = mount(LoginPage, {
      global: {
        mocks: { $q },
        stubs: ['q-page', 'q-btn', 'q-input', 'q-avatar', 'q-img', 'q-rating', 'q-checkbox', 'q-form'],
      }
    })

    wrapper.vm.email = 'missing@example.com'
    await wrapper.vm.onLogin()

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: expect.stringContaining('Email does not exist')
    }))
  })
})
