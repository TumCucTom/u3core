import { mount, MountingOptions } from '@vue/test-utils'
import { describe, it, expect, beforeEach, afterEach,vi, type Mock } from 'vitest'
import ResetPassword from '../ResetPassword.vue'
import axios from 'axios'
import { routerKey, routeLocationKey } from 'vue-router'

// mocks & stubs
vi.mock('axios')
vi.mock('bcryptjs')
const notifyMock = vi.fn()
const pushMock = vi.fn()
vi.mock('vue-router', async (importOriginal) => {
  const actual = (await importOriginal()) as Record<string, any>
  return {
    ...actual,
    useRoute: () => ({
      query: {
        token: 'abc123',
        email: encodeURIComponent('test@example.com'),
      }
    })
  }
})

vi.mock('quasar', async (importOriginal) => {
  const actual = (await importOriginal()) as Record<string, any>
  return {
    ...actual,
    useQuasar: () => ({
      notify: notifyMock
    })
  }
})


const axiosMock = axios as unknown as {
  get: ReturnType<typeof vi.fn>,
  post: ReturnType<typeof vi.fn>
}

const routeMock = {
  query: {
    token: '',
    email: ''
  }
}

// Centralized factory
const factory = (options: MountingOptions<any> = {}) => {
  return mount(ResetPassword, {
    global: {
      provide: {
        _q_: { notify: notifyMock },
        [routerKey]: { push: pushMock },
        [routeLocationKey]: routeMock,
      },
      stubs: {
        'q-page': { template: '<div><slot /></div>' },
        'q-toolbar': { template: '<div><slot /></div>' },
        'q-toolbar-title': { template: '<div><slot /></div>' },
        'q-icon': { template: '<span><slot /></span>' },
        'q-card': { template: '<div><slot /></div>' },
        'q-card-section': { template: '<div><slot /></div>' },
        'q-input': { template: '<input />' },
        'q-btn': { template: '<button><slot /></button>' },
        'router-link': true,
        'router-view': true,
      },
      ...options.global,
    },
    ...options,
  })
}


describe('ResetPassword.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    vi.resetAllMocks()
    wrapper = factory()
  })

  afterEach(() => {
    if (wrapper) {
      wrapper.unmount()
    }
  })

  it('renders main headings and password inputs', () => {
    expect(wrapper.text()).toContain('RESET PASSWORD')
    expect(wrapper.text()).toContain('Password Requirements')
    expect(wrapper.text()).toContain('Enter Your New Password')
  })

  it('toggles password visibility', async () => {
    expect((wrapper.vm as any).showPassword).toBe(false);
    (wrapper.vm as any).togglePassword()
    expect((wrapper.vm as any).showPassword).toBe(true)

    expect((wrapper.vm as any).showConfirmPassword).toBe(false);
    (wrapper.vm as any).toggleConfirmPassword()
    expect((wrapper.vm as any).showConfirmPassword).toBe(true)
  })

  it('shows error if email is not registered', async () => {
    axiosMock.get.mockResolvedValueOnce({ data: ['someoneelse@example.com'] })

    (wrapper.vm as any).newPassword = 'Password1!';
    (wrapper.vm as any).confirmPassword = 'Password1!'
    await (wrapper.vm as any).$nextTick(); //wait for Vue to update

    await (wrapper.vm as any).resetPassword()

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: 'Error resetting password'
    }))
  })

  it('shows error if passwords do not match', async () => {
    axiosMock.get.mockResolvedValueOnce({ data: ['test@example.com'] })

    (wrapper.vm as any).newPassword = 'Password1!';
    (wrapper.vm as any).confirmPassword = 'WrongPassword'

    await (wrapper.vm as any).resetPassword()

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: 'Error resetting password'
    }))
  })

  it('shows error if server fails during password reset', async () => {
    (axios.get as Mock).mockResolvedValueOnce({ data: ['test@example.com'] })
    ;(axios.post as Mock).mockRejectedValueOnce(new Error('Server Error'))

    // passwords must match so it doesn't early-return!
    (wrapper.vm as any).newPassword = 'GoodPassword1!';
    (wrapper.vm as any).confirmPassword = 'GoodPassword1!';


    await (wrapper.vm as any).resetPassword()

    expect(notifyMock).toHaveBeenCalledWith(expect.objectContaining({
      message: 'Passwords do not match or do not meet the requirements'
    }))
  })

})
