import { mount, MountingOptions} from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import ErrorNotFound from '../ErrorNotFound.vue'
import { routerKey, routeLocationKey } from 'vue-router'

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
const factory = (options:MountingOptions<any> = {}) => {
  return mount(ErrorNotFound, {
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

describe('ErrorNotFound.vue', () => {
  it('renders 404 and a home button', () => {
    const wrapper = factory()

    expect(wrapper.text()).toContain('404')
    expect(wrapper.text()).toContain('Oops. Nothing here...')
    expect(wrapper.text()).toContain('Go Home')
  })
})
