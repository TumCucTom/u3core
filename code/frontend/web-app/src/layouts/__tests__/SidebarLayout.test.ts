import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import SidebarLayout from '../SidebarLayout.vue'
import { createRouter, createMemoryHistory, routerKey } from 'vue-router'
import { Quasar } from 'quasar'

// 🛠 Create a fake router
const router = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: '/', component: { template: '<div>Home</div>' } }]
})

// 🛠 Mocks
const pushMock = vi.fn()

// 🛠 Centralized factory
const factory = (options = {}) => {
  return mount(SidebarLayout, {
    global: {
      plugins: [Quasar],
      provide: {
        [routerKey]: { push: pushMock }
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
      },
      ...options.global
    },
    ...options
  })
}

describe('SidebarLayout.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    vi.resetAllMocks()
    wrapper = factory()
  })

  it('renders the sidebar and router-view', () => {
    expect(wrapper.find('q-layout-stub').exists()).toBe(true)
    expect(wrapper.find('q-drawer-stub').exists()).toBe(true)
    expect(wrapper.find('router-view-stub').exists()).toBe(true)
  })

  it('shows filtered menu items based on search', async () => {
    await wrapper.setData({ searchQuery: 'Dashboard' })
    expect((wrapper.vm as any).filteredItems.length).toBe(1)
    expect((wrapper.vm as any).filteredItems[0].label).toBe('Dashboard')
  })

  it('opens and closes logout dialog', async () => {
    expect((wrapper.vm as any).showLogoutDialog).toBe(false)
    await wrapper.setData({ showLogoutDialog: true })
    expect(wrapper.find('q-dialog-stub').exists()).toBe(true)
  })

  it('confirms logout and redirects to login', async () => {
    await (wrapper.vm as any).confirmLogout()
    expect(pushMock).toHaveBeenCalledWith('/')
  })
})
