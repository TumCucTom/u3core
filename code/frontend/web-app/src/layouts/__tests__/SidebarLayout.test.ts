import { mount, MountingOptions } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import SidebarLayout from '../SidebarLayout.vue'
import {routerKey } from 'vue-router'

const notifyMock = vi.fn()
const pushMock   = vi.fn()

const factory = (options: MountingOptions<any> = {}) => {
  return mount(SidebarLayout, {
    shallow: true,
    global: {
      provide: {
        _q_: { notify: notifyMock },
        [routerKey]: { push: pushMock },
      },
      stubs: {
        'router-link': true,
        'router-view': true,
        'q-layout': true,
        'q-drawer': true,
        'q-dialog': true,
        'q-btn': true,
        'q-icon': true,
        'q-input': true,
        'q-list': true,
        'q-item': true,
        'q-item-section': true,
        'q-item-label': true,
        'q-page-container': true,
        'q-card': true,
        'q-card-section': true,
        'q-card-actions': true,
        'q-avatar': true,
        'q-img': true,
      },
      ...options.global,
    },
    ...options,
  })
}


describe('SidebarLayout.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    vi.resetAllMocks()
    wrapper = factory()
  })

  it('shows filtered menu items based on search', async () => {
    await wrapper.setData({ searchQuery: 'Dashboard' })
    expect((wrapper.vm as any).filteredItems.length).toBe(1)
  })

  it('opens and closes logout dialog', async () => {
    expect((wrapper.vm as any).showLogoutDialog).toBe(false)
  })
})
