import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import SettingsPage from '../SettingsPage.vue'

describe('SettingsPage.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    wrapper = mount(SettingsPage, {
      global: {
        stubs: ['q-page', 'q-tabs', 'q-tab', 'q-tab-panels', 'q-tab-panel', 'q-btn', 'q-card', 'q-toggle', 'q-icon', 'q-chip'],
      }
    })
  })

  it('renders main Settings title', () => {
    expect(wrapper.text()).toContain('Settings')
  })

  it('renders all tabs', () => {
    expect(wrapper.text()).toContain('Application Settings')
    expect(wrapper.text()).toContain('Camera Edge & device Management')
    expect(wrapper.text()).toContain('User Roles & Permissions')
    expect(wrapper.text()).toContain('Data Privacy & Compliance')
    expect(wrapper.text()).toContain('Integrations')
    expect(wrapper.text()).toContain('API')
  })

  it('switches tabs correctly', async () => {
    expect(wrapper.vm.currentTab).toBe('application')

    wrapper.vm.currentTab = 'privacy'
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.currentTab).toBe('privacy')
  })

  it('toggles notification settings', async () => {
    expect(wrapper.vm.allEventsPush).toBe(true)

    wrapper.vm.allEventsPush = false
    wrapper.vm.allEventsEmail = false
    wrapper.vm.allEventsSMS = true

    await wrapper.vm.$nextTick()

    expect(wrapper.vm.allEventsPush).toBe(false)
    expect(wrapper.vm.allEventsEmail).toBe(false)
    expect(wrapper.vm.allEventsSMS).toBe(true)
  })

  it('selects different data retention plans', async () => {
    expect(wrapper.vm.dataRetention).toBe('basic')

    wrapper.vm.dataRetention = 'enterprise'
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.dataRetention).toBe('enterprise')
  })

  it('toggles Data Privacy options (At Rest, In Transit, Anonymised Data)', async () => {
    expect(wrapper.vm.dataRest).toBe(false)
    expect(wrapper.vm.dataTransit).toBe(false)
    expect(wrapper.vm.anonymisedData).toBe(false)

    wrapper.vm.dataRest = true
    wrapper.vm.dataTransit = true
    wrapper.vm.anonymisedData = true

    await wrapper.vm.$nextTick()

    expect(wrapper.vm.dataRest).toBe(true)
    expect(wrapper.vm.dataTransit).toBe(true)
    expect(wrapper.vm.anonymisedData).toBe(true)
  })
})
