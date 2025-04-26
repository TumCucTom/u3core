// src/pages/__tests__/ActionsSettingPage.test.ts

import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import ActionsSettingPage from '../ActionSettingsPage.vue';

describe('ActionsSettingPage', () => {
  const mountPage = () =>
    mount(ActionsSettingPage, {
      global: {
        stubs: ['q-page', 'q-btn', 'q-input', 'q-table', 'q-icon'], // Stub Quasar components
      },
    });

  it('renders the page and title section correctly', () => {
    const wrapper = mountPage();
    expect(wrapper.text()).toContain('Actions Setting');
    expect(wrapper.text()).toContain('Track, manage and forecast your customers and orders.');
    expect(wrapper.find('h1').text()).toBe('Actions Setting');
  });

  it('renders the + Add Recipient button', () => {
    const wrapper = mountPage();
    const addButton = wrapper.findComponent({ name: 'q-btn' });
    expect(addButton.exists()).toBe(true);
  });

  it('renders filter buttons (SMS, Email, Whatsapp, Twitter)', () => {
    const wrapper = mountPage();
    expect(wrapper.text()).toContain('SMS');
    expect(wrapper.text()).toContain('Email');
    expect(wrapper.text()).toContain('Whatsapp');
    expect(wrapper.text()).toContain('Twitter');
  });

  it('renders search input and filter buttons', () => {
    const wrapper = mountPage();
    expect(wrapper.text()).toContain('Search');
    expect(wrapper.text()).toContain('All');
    expect(wrapper.text()).toContain('More filters');
  });

  it('renders the table with no data', () => {
    const wrapper = mountPage();
    expect(wrapper.text()).toContain('No data available');
  });

  it('renders pagination controls', () => {
    const wrapper = mountPage();
    expect(wrapper.text()).toContain('Previous');
    expect(wrapper.text()).toContain('Next');
    expect(wrapper.text()).toContain('Page 1 of 10');
  });

});
