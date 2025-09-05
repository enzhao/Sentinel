import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createTestingPinia, type TestingPinia } from '@pinia/testing';
import { createSentinelRouter } from '@/router';
import { setActivePinia } from 'pinia';
import DashboardView from '@/views/DashboardView.vue';
import PortfoliosListView from '@/views/PortfoliosListView.vue';
import { usePortfolioStore } from '@/stores/portfolios';

// This is a high-fidelity view test.
// Reference: docs/testing_strategy.md (Section 4.3)

// Mock the fetch API at the boundary
const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('DashboardView.vue', () => {
  let router;
  let pinia: TestingPinia;

  beforeEach(async () => {
    // Pinia must be created and activated before the router is created
    // so that the router's navigation guards can use the stores.
    pinia = createTestingPinia({
      createSpy: vi.fn,
    });
    setActivePinia(pinia);

    router = createSentinelRouter();
    await router.push({ name: 'dashboard' });
    await router.isReady();
    
    // Mock a successful (but empty) fetch for the embedded portfolio list
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([]),
    });
  });

  it('renders placeholder cards and the portfolio list view', async () => {
    const wrapper = mount(DashboardView, {
      global: { plugins: [pinia, router] },
    });

    // Check for placeholder cards
    expect(wrapper.text()).toContain('Overall Performance');
    expect(wrapper.text()).toContain('Key Metric 1');

    // Check that the PortfoliosListView component is rendered
    expect(wrapper.findComponent(PortfoliosListView).exists()).toBe(true);

    // Verify that the store action was called by the child component
    const portfolioStore = usePortfolioStore();
    expect(portfolioStore.fetchPortfolios).toHaveBeenCalledOnce();
  });
});