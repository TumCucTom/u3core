import { mount, MountingOptions } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import VerifiedPassword from '../VerifiedPassword.vue'
import { routerKey, routeLocationKey } from 'vue-router'
import axios from 'axios'
import { Quasar } from 'quasar'

vi.mock('axios')


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
const factory = (options: MountingOptions<any> = {}) => {
  return mount(VerifiedPassword, {
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

describe('VerifiedPassword.vue', () => {
  beforeEach(() => {
    vi.resetAllMocks()
    // Reset the route between tests
    routeMock.query.token = ''
    routeMock.query.email = ''
  })

  it('redirects to dashboard if token and email are present', async () => {
    routeMock.query.token = 'test-token'
    routeMock.query.email = encodeURIComponent('test@example.com')

    factory()

    expect(pushMock).toHaveBeenCalledWith('/app/dashboard?email=test@example.com')
  })

  it('redirects to home if token or email are missing', async () => {
    routeMock.query.token = ''
    routeMock.query.email = ''

    factory()

    expect(pushMock).toHaveBeenCalledWith('/')
  })
})
