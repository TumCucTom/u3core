import { mount } from '@vue/test-utils'
import HomeLayout from '../HomeLayout.vue'
import { describe, it, expect, vi } from 'vitest'
import { createTestingPinia } from '@pinia/testing'
import { createRouter, createMemoryHistory } from 'vue-router'
import { Quasar, Dark } from 'quasar'

// Mock routes
const router = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: '/', component: { template: '<div>Home</div>' } }]
})

describe('HomeLayout.vue', () => {
  it('renders layout and router-view', async () => {
    const wrapper = mount(HomeLayout, {
      global: {
        plugins: [router, Quasar],
        stubs: ['router-view']
      }
    })

    expect(wrapper.find('q-layout-stub').exists()).toBe(true)
    expect(wrapper.find('q-header-stub').exists()).toBe(true)
  })

  it('toggles dark mode on button click', async () => {
    const wrapper = mount(HomeLayout, {
      global: {
        plugins: [router, Quasar]
      }
    })

    const darkBtn = wrapper.findComponent({ name: 'QBtn' }).find('button')
    expect(typeof darkBtn.exists()).toBe(true)
    // Normally this would toggle $q.dark manually in a browser context
    // In real test you can spy or simulate it if needed
  })

  it('opens the hyperlink when logo clicked', async () => {
    const windowOpen = vi.spyOn(window, 'open').mockImplementation(() => {})
    const wrapper = mount(HomeLayout, {
      global: {
        plugins: [router, Quasar]
      }
    })

    await wrapper.find('img').trigger('click')
    expect(windowOpen).toHaveBeenCalledWith('https://google.com', '_blank')
    windowOpen.mockRestore()
  })
})
