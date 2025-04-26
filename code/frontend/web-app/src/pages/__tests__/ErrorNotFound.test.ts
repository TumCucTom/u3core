import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import ErrorNotFound from '../ErrorNotFound.vue'

// Centralized factory
const factory = (options = {}) => {
  return mount(ErrorNotFound, {
    global: {
      provide: {
        _q_: {}, // mock useQuasar() if needed (safe even if ErrorNotFound doesn't use it)
      },
      stubs: ['q-btn'], // stub all Quasar components used inside
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
