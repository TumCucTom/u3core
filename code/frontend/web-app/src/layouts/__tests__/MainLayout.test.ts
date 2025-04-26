import { mount } from '@vue/test-utils'
import MainLayout from '../MainLayout.vue'
import EssentialLink from '../../components/EssentialLink.vue'
import { describe, it, expect } from 'vitest'
import { Quasar } from 'quasar'
import { createRouter, createMemoryHistory } from 'vue-router'

const router = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: '/', component: { template: '<div>Home</div>' } }]
})

describe('MainLayout.vue', () => {
  it('renders layout with toolbar and drawer closed initially', () => {
    const wrapper = mount(MainLayout, {
      global: {
        plugins: [Quasar, router],
        stubs: {
          EssentialLink,
          RouterView: true
        }
      }
    })

    expect(wrapper.find('q-layout-stub').exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'QToolbar' }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'QDrawer' }).exists()).toBe(true)
    expect(wrapper.vm.leftDrawerOpen).toBe(false)
  })

  it('toggles drawer when menu button clicked', async () => {
    const wrapper = mount(MainLayout, {
      global: {
        plugins: [Quasar, router],
        stubs: {
          EssentialLink,
          RouterView: true
        }
      }
    })

    const btn = wrapper.findComponent({ name: 'QBtn' })
    await btn.trigger('click')
    expect(wrapper.vm.leftDrawerOpen).toBe(true)
  })

  it('renders all EssentialLink components', () => {
    const wrapper = mount(MainLayout, {
      global: {
        plugins: [Quasar, router],
        stubs: {
          EssentialLink,
          RouterView: true
        }
      }
    })

    const linkCount = wrapper.findAllComponents(EssentialLink).length
    expect(linkCount).toBe(7) // update if you change `linksList.length`
  })
})
