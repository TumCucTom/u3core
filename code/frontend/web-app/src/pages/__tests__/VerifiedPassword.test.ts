import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import VerifiedPassword from '../VerifiedPassword.vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

import { Quasar } from 'quasar'

const wrapper = mount(VerifiedPassword, {
  global: {
    plugins: [Quasar],
  }
})

vi.mock('axios')

describe('VerifiedPassword.vue', () => {
  it('redirects to dashboard if token and email are present', async () => {
    const router = useRouter()
    const route = useRoute()

    route.query.token = 'test-token'
    route.query.email = encodeURIComponent('test@example.com')

    mount(VerifiedPassword)

    expect(router.push).toHaveBeenCalledWith('/app/dashboard?email=test@example.com')
  })

  it('redirects to home if token or email are missing', async () => {
    const router = useRouter()
    const route = useRoute()

    route.query.token = ''
    route.query.email = ''

    mount(VerifiedPassword)

    expect(router.push).toHaveBeenCalledWith('/')
  })
})
