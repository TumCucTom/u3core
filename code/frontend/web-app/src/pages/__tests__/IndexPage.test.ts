import { mount, MountingOptions} from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import IndexPage from '../IndexPage.vue'
import axios from 'axios'
import { Quasar } from 'quasar'
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
const factory = (options: MountingOptions<any> = {}) => {
  return mount(IndexPage, {
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

describe('IndexPage.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    wrapper = factory()
  })
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the logo image', () => {
    const wrapper = factory()

    const img = wrapper.find('img')
    expect(img.exists()).toBe(true)
    expect(img.attributes('alt')).toBe('Quasar logo')
  })
})
