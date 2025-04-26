import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import CloudSettings from '../CloudSettings.vue';

describe('CloudSettings', () => {
  let wrapper: ReturnType<typeof mount>;

  beforeEach(() => {
    wrapper = mount(CloudSettings, {
      global: {
        stubs: ['q-page', 'q-card', 'q-form', 'q-btn', 'q-btn-group', 'q-select', 'q-input', 'q-option-group', 'q-chip', 'q-card-section', 'q-separator'],
      },
    });
  });

  it('renders the title and subtitle', () => {
    expect(wrapper.text()).toContain('Cloud Settings');
    expect(wrapper.text()).toContain('Configure cloud settings for anomaly detection.');
  });

  it('renders EC2 instance select input with correct default', () => {
    expect(wrapper.vm.ec2Instance).toBe('t2.micro');
  });

  it('renders cloud endpoint input with correct default', () => {
    expect(wrapper.vm.cloudEndpointUrl).toBe('https://api.cloudprovider.com/v1/upload');
  });

  it('renders timing options with "shift-based" selected', () => {
    expect(wrapper.vm.timingsType).toBe('shift-based');
  });

  it('shows start and end time inputs when "shift-based" is selected', () => {
    expect(wrapper.text()).toContain('Start time');
    expect(wrapper.text()).toContain('End time');
    expect(wrapper.vm.startTime).toBe('09:00');
    expect(wrapper.vm.endTime).toBe('17:00');
  });

  it('renders API key input with correct default', () => {
    expect(wrapper.vm.apiKey).toBe('ABCD1234XYZ5678');
  });

  it('renders data usage value', () => {
    expect(wrapper.text()).toContain('0 GB');
  });

  it('renders the retention policy buttons', () => {
    expect(wrapper.text()).toContain('7 days');
    expect(wrapper.text()).toContain('30 days');
    expect(wrapper.text()).toContain('90 days');
    expect(wrapper.vm.retentionPolicy).toBe('7days');
  });

  it('handles form submission and logs correct values', async () => {
    const logSpy = vi.spyOn(console, 'log');

    await wrapper.findComponent({ name: 'q-form' }).trigger('submit.prevent');

    expect(logSpy).toHaveBeenCalledWith('EC2 Instance:', 't2.micro');
    expect(logSpy).toHaveBeenCalledWith('Cloud Endpoint URL:', 'https://api.cloudprovider.com/v1/upload');
    expect(logSpy).toHaveBeenCalledWith('Timings Type:', 'shift-based');
    expect(logSpy).toHaveBeenCalledWith('Start Time:', '09:00');
    expect(logSpy).toHaveBeenCalledWith('End Time:', '17:00');
    expect(logSpy).toHaveBeenCalledWith('API Key:', 'ABCD1234XYZ5678');
    expect(logSpy).toHaveBeenCalledWith('Retention Policy:', '7days');

    logSpy.mockRestore();
  });
});
