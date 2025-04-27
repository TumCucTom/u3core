// src/pages/__tests__/ActionsSettingPage.test.ts

import { mount, MountingOptions } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import ActionsSettingPage from '../ActionSettingsPage.vue'
import axios from 'axios'
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
const factory = (options: MountingOptions<any> = {}) => {
  return mount(ActionsSettingPage, {
    global: {
      provide: {
        _q_: { notify: notifyMock },
        [routerKey]: { push: pushMock },
        [routeLocationKey]: routeMock,
      },
      stubs: {
        'q-page': { template: '<div><slot /></div>' },
        'q-btn': {
          name: 'q-btn',
          props: ['label'],
          template: '<button>{{ label }}</button>'
        },
        'q-input': {
          name: 'q-input',
          props: ['placeholder'],
          template: '<input :placeholder="placeholder" />'
        },
        'q-table': {
          name: 'q-table',
          template: '<div><slot /></div>'
        },
        'q-td': {
          name: 'q-td',
          template: '<td><slot /></td>'
        },
        'q-icon': {
          name: 'q-icon',
          props: ['name'],
          template: '<span>{{ name }}</span>'
        },
        'q-avatar': true,
        'q-img': true,
        'q-rating': true,
        'q-checkbox': true,
        'q-form': { template: '<form><slot /></form>' },
      }
      ,
      ...options.global,
    },
    ...options,
  })
}

describe('ActionsSettingPage', () => {
  let wrapper: ReturnType<typeof mount>
  beforeEach(() => {
    wrapper = factory()
  })
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the page and title section correctly', () => {
    const wrapper = factory()
    expect(wrapper.text()).toContain('Actions Setting')
    expect(wrapper.text()).toContain('Track, manage and forecast your customers and orders.')
    expect(wrapper.find('h1').text()).toBe('Actions Setting')
  })

  it('renders the + Add Recipient button', () => {
    const wrapper = factory()
    const addButton = wrapper.findComponent({ name: 'q-btn' })
    expect(addButton.exists()).toBe(true)
  })

  it('renders filter buttons (SMS, Email, Whatsapp, Twitter)', () => {
    const wrapper = factory()
    expect(wrapper.text()).toContain('SMS')
    expect(wrapper.text()).toContain('Email')
    expect(wrapper.text()).toContain('Whatsapp')
    expect(wrapper.text()).toContain('Twitter')
  })

  it('renders search input and filter buttons', () => {
    const wrapper = factory()
    expect(wrapper.text()).toContain('All')
    expect(wrapper.text()).toContain('More filters')
  })

  it('renders pagination controls', () => {
    const wrapper = factory()
    expect(wrapper.text()).toContain('Previous')
    expect(wrapper.text()).toContain('Next')
    expect(wrapper.text()).toContain('Page 1 of 10')
  })
})
