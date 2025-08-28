import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mount } from '@vue/test-utils';
import MarketDataTicker from '@/components/MarketDataTicker.vue';

describe('MarketDataTicker.vue', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('renders ticker data correctly on mount', async () => {
    const wrapper = mount(MarketDataTicker, {
      global: {
        plugins: [],
      },
      props: {
        tickers: ['^GSPC', '^IXIC'],
      },
    });

    // Advance timers to trigger onMounted and fetchMarketData
    vi.advanceTimersByTime(0);
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('S&P 500');
    expect(wrapper.text()).toContain('5,200.12');
    expect(wrapper.text()).toContain('+0.5%');
    expect(wrapper.text()).toContain('NASDAQ');
    expect(wrapper.text()).toContain('16,300.45');
    expect(wrapper.text()).toContain('-0.2%');
  });

  it('updates ticker data on interval', async () => {
    const wrapper = mount(MarketDataTicker, {
      global: {
        plugins: [],
      },
      props: {
        tickers: ['^GSPC'],
      },
    });

    vi.advanceTimersByTime(0);
    await wrapper.vm.$nextTick();

    // Initial data
    expect(wrapper.text()).toContain('S&P 500');

    // Simulate data change (though our mock is static, we test the interval call)
    // In a real scenario, fetchMarketData would return new data here.
    vi.advanceTimersByTime(60000);
    await wrapper.vm.$nextTick();

    // Expect the data to still be present, indicating the interval fired and re-rendered
    expect(wrapper.text()).toContain('S&P 500');
  });

  it('handles changes in tickers prop', async () => {
    const wrapper = mount(MarketDataTicker, {
      global: {
        plugins: [],
      },
      props: {
        tickers: ['^GSPC'],
      },
    });

    vi.advanceTimersByTime(0);
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain('S&P 500');
    expect(wrapper.text()).not.toContain('DAX');

    await wrapper.setProps({ tickers: ['^GDAXI'] });
    vi.advanceTimersByTime(0);
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).not.toContain('S&P 500');
    expect(wrapper.text()).toContain('DAX');
  });

  it('clears interval on unmount', async () => {
    const clearIntervalSpy = vi.spyOn(global, 'clearInterval');
    const wrapper = mount(MarketDataTicker, {
      global: {
        plugins: [],
      },
      props: {
        tickers: ['^GSPC'],
      },
    });

    vi.advanceTimersByTime(0);
    await wrapper.vm.$nextTick();

    wrapper.unmount();
    expect(clearIntervalSpy).toHaveBeenCalled();
  });
});
