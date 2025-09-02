import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createTestingPinia, setActivePinia } from '@pinia/testing';
import { createSentinelRouter } from '@/router';
import PortfoliosListView from '@/views/PortfoliosListView.vue';
import { usePortfolioStore } from '@/stores/portfolios';
import type { PortfolioSummary } from '@/api/models';

// This is a high-fidelity view test.
// Reference: docs/testing_strategy.md (Section 4.3)

// Mock the fetch API at the boundary
const mockFetch = vi.fn();
global.fetch = mockFetch;

// Mock Firebase auth for apiService
vi.mock('@/plugins/firebase', () => ({
  auth: {
    currentUser: {
      getIdToken: vi.fn().mockResolvedValue('mock-token'),
    },
  },
}));

const mockPortfolios: PortfolioSummary[] = [
  { portfolioId: 'pf-1', name: 'Growth Stocks', currentValue: 125000 },
  { portfolioId: 'pf-2', name: 'Paper Trading', currentValue: 9800 },
];

describe('PortfoliosListView.vue', () => {
  let router;
  let pinia;

  beforeEach(async () => {
    vi.resetAllMocks();
    // Pinia must be created and activated before the router is created
    // so that the router's navigation guards can use the stores.
    pinia = createTestingPinia({ createSpy: vi.fn });
    setActivePinia(pinia);

    router = createSentinelRouter();
    await router.push({ name: 'dashboard' }); // A route where this component might live
    await router.isReady();
  });

  it('shows loading indicator and then displays portfolios', async () => {
    // Arrange: mock a successful fetch
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockPortfolios),
    });

    const wrapper = mount(PortfoliosListView, {
      global: { plugins: [pinia, router] },
    });

    const store = usePortfolioStore();
    store.loading = true; // Manually set loading to test the indicator
    await wrapper.vm.$nextTick();

    // Assert: loading indicator is visible
    expect(wrapper.findComponent({ name: 'VProgressLinear' }).exists()).toBe(true);

    // Let the fetch complete
    store.loading = false;
    store.portfolioList = mockPortfolios;
    await wrapper.vm.$nextTick();

    // Assert: list is now visible
    expect(wrapper.findComponent({ name: 'VProgressLinear' }).exists()).toBe(false);
    expect(wrapper.text()).toContain('Growth Stocks');
    expect(wrapper.text()).toContain('Paper Trading');
  });

  it('navigates to portfolio detail on item click', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve(mockPortfolios) });
    const wrapper = mount(PortfoliosListView, { global: { plugins: [pinia, router] } });
    const push = vi.spyOn(router, 'push');
    usePortfolioStore().portfolioList = mockPortfolios; // Set state
    await wrapper.vm.$nextTick();

    const firstItem = wrapper.findComponent({ name: 'VListItem' });
    await firstItem.trigger('click');

    expect(push).toHaveBeenCalledWith({ name: 'portfolio-detail', params: { id: 'pf-1' } });
  });

  it('opens confirmation dialog on delete click and deletes portfolio on confirm', async () => {
    // Arrange
    mockFetch.mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(mockPortfolios) });
    const wrapper = mount(PortfoliosListView, { global: { plugins: [pinia, router] } });
    const store = usePortfolioStore();
    store.portfolioList = mockPortfolios;
    await wrapper.vm.$nextTick();

    // Act 1: Enter manage mode and click delete
    await wrapper.find('button.v-btn', { text: 'Manage' }).trigger('click');
    await wrapper.find('button[icon="mdi-delete-outline"]').trigger('click');
    await wrapper.vm.$nextTick();

    // Assert 1: Dialog is visible
    const dialog = wrapper.findComponent({ name: 'ConfirmationDialog' });
    expect(dialog.exists()).toBe(true);
    expect(dialog.text()).toContain("Are you sure you want to delete the portfolio 'Growth Stocks'?");

    // Arrange 2: Mock the DELETE and subsequent GET fetch calls
    mockFetch
      .mockResolvedValueOnce({ ok: true, status: 204, json: () => Promise.resolve() }) // For DELETE
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve([mockPortfolios[1]]) }); // For GET refresh

    // Act 2: Confirm deletion
    await dialog.vm.$emit('confirm');
    
    // Assert 2: Store action was called
    expect(store.deletePortfolio).toHaveBeenCalledWith('pf-1');
  });
});