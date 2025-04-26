import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import VerifiedPassword from '../VerifiedPassword.vue'
import { routerKey, routeLocationKey } from 'vue-router'
import axios from 'axios'
import { Quasar } from 'quasar'

vi.mock('axios')

// Create fresh mocks per test
const pushMock = vi.fn()
const routeMock = {
  query: {
    token: '',
    email: ''
  }
}

// Centralized factory
const factory = () => {
  return mount(VerifiedPassword, {
    global: {
      plugins: [Quasar],
      provide: {
        [routerKey]: { push: pushMock },
        [routeLocationKey]: routeMock,
      },
      stubs: ['q-page', 'q-btn'] // or whatever Quasar components you use inside
    }
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
