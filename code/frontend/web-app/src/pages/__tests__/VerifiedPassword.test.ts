import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import VerifiedPassword from '../VerifiedPassword.vue'
import { createRouter, createMemoryHistory } from 'vue-router'

describe('VerifiedPassword.vue', () => {
  it('redirects to dashboard if token and email are present', async () => {
    const push = vi.fn()

    vi.mock('vue-router', async () => {
      const actual = await vi.importActual('vue-router')
      return {
        ...actual,
        useRouter: () => ({ push }),
        useRoute: () => ({
          query: {
            token: 'test-token',
            email: encodeURIComponent('test@example.com')
          }
        })
      }
    })

    mount(VerifiedPassword)

    expect(push).toHaveBeenCalledWith('/app/dashboard?email=test@example.com')
  })

  it('redirects to home if token or email are missing', async () => {
    const push = vi.fn()

    vi.mock('vue-router', async () => {
      const actual = await vi.importActual('vue-router')
      return {
        ...actual,
        useRouter: () => ({ push }),
        useRoute: () => ({
          query: {
            token: '', // missing
            email: ''
          }
        })
      }
    })

    mount(VerifiedPassword)

    expect(push).toHaveBeenCalledWith('/')
  })
})
