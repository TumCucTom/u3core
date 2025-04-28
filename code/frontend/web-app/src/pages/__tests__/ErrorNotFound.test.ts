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
      provide: {
        _q_: { notify: notifyMock },
        [routerKey]: { push: pushMock },
        [routeLocationKey]: routeMock,
      },
      stubs: {
        'q-page': true,
        'q-input': true,
        'q-avatar': true,
        'q-img': true,
        'q-rating': true,
        'q-checkbox': true,
        'q-form': true,
        'q-btn': {
          template: '<button>{{ label }}</button>', 
          props: ['label'],
        },
      },
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
