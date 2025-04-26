import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import ErrorNotFound from '../ErrorNotFound.vue';

describe('ErrorNotFound.vue', () => {
  it('renders 404 and a home button', () => {
    const wrapper = mount(ErrorNotFound, {
      global: {
        stubs: ['q-btn'], // stub Quasar component
      },
    });

    expect(wrapper.text()).toContain('404');
    expect(wrapper.text()).toContain('Oops. Nothing here...');
    expect(wrapper.text()).toContain('Go Home');
  });
});
