import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import IndexPage from '../IndexPage.vue';
import axios from 'axios'
import { vi } from 'vitest'

vi.mock('axios')

describe('IndexPage.vue', () => {
  it('renders the logo image', () => {
    const wrapper = mount(IndexPage, {
      global: {
        stubs: ['q-page'],
      },
    });

    const img = wrapper.find('img');
    expect(img.exists()).toBe(true);
    expect(img.attributes('alt')).toBe('Quasar logo');
  });
});
