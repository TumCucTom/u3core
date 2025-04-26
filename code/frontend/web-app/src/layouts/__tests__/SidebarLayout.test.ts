import { mount } from '@vue/test-utils'
import SidebarLayout from '../layouts/SidebarLayout.vue'
import { describe, it, expect, vi } from 'vitest'
import { createRouter, createMemoryHistory } from 'vue-router'
import { Quasar } from 'quasar'

const router = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: '/', component: { template: '<div>Home</div>' } }]
})

describe('SidebarLayout.vue', () => {
  it('renders the sidebar and router-view', () => {
    const wrapper = mount(SidebarLayout, {
      global: {
        plugins: [router, Quasar],
        stubs: {
          RouterLink: true,
          RouterView: true
        }
      }
    })

    expect(wrapper.find('q-layout-stub').exists()).toBe(true)
    expect(wrapper.find('q-drawer-stub').exists()).toBe(true)
    expect(wrapper.find('router-view-stub').exists()).toBe(true)
  })

  it('shows filtered menu items based on search', async () => {
    const wrapper = mount(SidebarLayout, {
      global: {
        plugins: [router, Quasar],
        stubs: {
          RouterLink: true,
          RouterView: true
        }
      }
    })

    await wrapper.setData({ searchQuery: 'Dashboard' })
    expect(wrapper.vm.filteredItems.length).toBe(1)
    expect(wrapper.vm.filteredItems[0].label).toBe('Dashboard')
  })

  it('opens and closes logout dialog', async () => {
    const wrapper = mount(SidebarLayout, {
      global: {
        plugins: [router, Quasar],
        stubs: {
          RouterLink: true,
          RouterView: true
        }
      }
    })

    expect(wrapper.vm.showLogoutDialog).toBe(false)
    await wrapper.setData({ showLogoutDialog: true })
    expect(wrapper.find('q-dialog-stub').exists()).toBe(true)
  })

  it('confirms logout and redirects to login', async () => {
    const push = vi.fn()
    const localRouter = {
      push
    }

    const wrapper = mount(SidebarLayout, {
      global: {
        mocks: { $router: localRouter },
        plugins: [router, Quasar],
        stubs: {
          RouterLink: true,
          RouterView: true
        }
      }
    })

    await wrapper.vm.confirmLogout()
    expect(push).toHaveBeenCalledWith('/')
  })
})
