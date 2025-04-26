import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import LoginPage from '../LoginPage.vue'
import axios from 'axios'
import bcrypt from 'bcryptjs'

// Mock libraries
vi.mock('axios')
vi.mock('bcryptjs')

const notifyMock = vi.fn()
const pushMock = vi.fn()

const $q = { notify: notifyMock }
const $router = { push: pushMock }

// Centralized factory for creating wrapper
const factory = (options = {}) => {
  return mount(LoginPage, {
    global: {
      mocks: { $q, $router },
      stubs: ['q-page', 'q-btn', 'q-input', 'q-avatar', 'q-img', 'q-rating', 'q-checkbox', 'q-form'],
      ...options.global,
    },
    ...options,
  })
}

describe('LoginPage.vue', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('Rendering and Mode Toggle', () => {
    it('renders correctly in signup mode by default', () => {
      const wrapper = factory()

      expect(wrapper.vm.isLogin).toBe(false)
      expect(wrapper.text()).toContain('Sign up')
      expect(wrapper.text()).toContain('First Name')
      expect(wrapper.text()).toContain('Last Name')
    })

    it('toggles to login mode', async () => {
      const wrapper = factory()

      expect(wrapper.vm.isLogin).toBe(false)
      await wrapper.vm.toggleMode()
      expect(wrapper.vm.isLogin).toBe(true)
      expect(wrapper.text()).toContain('Welcome back')
    })
  })

  describe('Signup Flow', () => {
    it('handles successful signup flow', async () => {
      axios.get.mockResolvedValueOnce({ data: ['someoneelse@example.com'] })
      axios.post.mockResolvedValueOnce({ data: 'success' })

      const wrapper = factory()

      wrapper.vm.email = 'newuser@example.com'
      wrapper.vm.firstName = 'John'
      wrapper.vm.lastName = 'Doe'
      wrapper.vm.password = 'Password1!'

      await wrapper.vm.onSubmit()

      expect(axios.post).toHaveBeenCalledWith(
        'http://16.171.224.57:80/api/addToCustomer', // ✅ Fixed port
        { items: ['John', 'Doe', 'newuser@example.com', 'Password1!'] }
      )
      expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
        message: expect.stringContaining('Email registered')
      }))
    })

    it('handles duplicate email on signup', async () => {
      axios.get.mockResolvedValueOnce({ data: ['test@example.com'] })

      const wrapper = factory()

      wrapper.vm.email = 'test@example.com'
      await wrapper.vm.onSubmit()

      expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
        message: expect.stringContaining('already registered')
      }))
    })

    it('handles signup server error', async () => {
      axios.get.mockResolvedValueOnce({ data: [] })
      axios.post.mockRejectedValueOnce(new Error('Server error'))

      const wrapper = factory()

      wrapper.vm.email = 'erroruser@example.com'
      wrapper.vm.firstName = 'Error'
      wrapper.vm.lastName = 'User'
      wrapper.vm.password = 'Password1!'

      await wrapper.vm.onSubmit()

      expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
        message: expect.stringContaining('Failed to register')
      }))
    })
  })

  describe('Login Flow', () => {
    it('handles successful login flow', async () => {
      axios.get.mockResolvedValueOnce({ data: '$2a$10$hashedpassword' })
      bcrypt.compare.mockResolvedValueOnce(true)

      const wrapper = factory()

      wrapper.vm.email = 'test@example.com'
      wrapper.vm.password = 'Password1!'
      await wrapper.vm.onLogin()

      expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
        message: expect.stringContaining('Successfully logged in')
      }))
      expect(pushMock).toHaveBeenCalledWith('/otp')
    })

    it('handles invalid password login flow', async () => {
      axios.get.mockResolvedValueOnce({ data: '$2a$10$hashedpassword' })
      bcrypt.compare.mockResolvedValueOnce(false)

      const wrapper = factory()

      wrapper.vm.email = 'test@example.com'
      wrapper.vm.password = 'wrongpassword'
      await wrapper.vm.onLogin()

      expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
        message: expect.stringContaining('Invalid username/password')
      }))
    })

    it('handles login error (email not found)', async () => {
      axios.get.mockRejectedValueOnce(new Error('Not Found'))

      const wrapper = factory()

      wrapper.vm.email = 'missing@example.com'
      await wrapper.vm.onLogin()

      expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
        message: expect.stringContaining('Email does not exist')
      }))
    })

    it('handles unexpected bcrypt error', async () => {
      axios.get.mockResolvedValueOnce({ data: '$2a$10$hashedpassword' })
      bcrypt.compare.mockRejectedValueOnce(new Error('bcrypt error'))

      const wrapper = factory()

      wrapper.vm.email = 'bcryptfail@example.com'
      wrapper.vm.password = 'Password1!'
      await wrapper.vm.onLogin()

      expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
        message: expect.stringContaining('Login failed')
      }))
    })
  })
})
