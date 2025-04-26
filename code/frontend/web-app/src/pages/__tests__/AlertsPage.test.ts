import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import AlertsPage from '../AlertsPage.vue';

vi.mock('axios')


// Mock global fetch
global.fetch = vi.fn();

describe('AlertsPage', () => {
  let wrapper: any;

  beforeEach(() => {
    wrapper = mount(AlertsPage, {
      global: {
        stubs: ['q-page', 'q-table', 'q-td', 'q-chip'], // Stub Quasar components
      },
    });
  });

  afterEach(() => {
    vi.clearAllMocks();
    wrapper.unmount();
  });

  it('renders the page title and subtitle', () => {
    expect(wrapper.text()).toContain('Alerts');
    expect(wrapper.text()).toContain('Track and manage your alerts');
  });

  it('renders the table component', () => {
    const table = wrapper.findComponent({ name: 'q-table' });
    expect(table.exists()).toBe(true);
  });

  it('calls fetchAlerts on mount', async () => {
    const mockData = [
      {
        id: 1,
        cameraName: 'Cam 1',
        cameraAddress: '123 Street',
        timestamp: '2023-01-01 10:00:00',
        faultType: 'Motion',
        numberOfHazards: 5,
        falsePositives: 1,
      },
    ];

    (fetch as unknown as vi.Mock).mockResolvedValue({
      json: () => Promise.resolve(mockData),
    });

    // Manually trigger fetchAlerts
    await wrapper.vm.fetchAlerts();
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.alertsData).toEqual(mockData);
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it('sets up polling on mount and clears on unmount', async () => {
    const clearIntervalSpy = vi.spyOn(window, 'clearInterval');

    const intervalId = wrapper.vm.pollInterval;
    expect(intervalId).toBeTruthy();

    wrapper.unmount();
    expect(clearIntervalSpy).toHaveBeenCalledWith(intervalId);

    clearIntervalSpy.mockRestore();
  });

  it('handles fetch error gracefully', async () => {
    (fetch as unknown as vi.Mock).mockRejectedValue(new Error('Network Error'));

    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    await wrapper.vm.fetchAlerts();

    expect(consoleErrorSpy).toHaveBeenCalledWith('Error fetching alerts:', expect.any(Error));

    consoleErrorSpy.mockRestore();
  });

});
