import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createTestingPinia, setActivePinia } from '@pinia/testing';
import { createSentinelRouter } from '@/router';
import PortfolioDetailsView from '@/views/PortfolioDetailsView.vue';
import { usePortfolioStore } from '@/stores/portfolios';
import type { Portfolio } from '@/api/models';

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

const mockPortfolio: Portfolio = {
  portfolioId: 'pf-1',
  userId: 'user-1',
  name: 'Detailed Portfolio',
  description: 'A test portfolio for details.',
  defaultCurrency: 'USD',
  cashReserve: { totalAmount: 50000, warChestAmount: 10000 },
  ruleSetId: null,
  createdAt: new Date().toISOString(),
  modifiedAt: new Date().toISOString(),
};

describe('PortfolioDetailsView.vue', () => {
  let router;
  let pinia;

  beforeEach(async () => {
    vi.resetAllMocks();
    // Pinia must be created and activated before the router is created
    // so that the router's navigation guards can use the stores.
    pinia = createTestingPinia({ createSpy: vi.fn });
    setActivePinia(pinia);

    router = createSentinelRouter();
    
    // Navigate to the detail route before mounting
    await router.push({ name: 'portfolio-detail', params: { id: 'pf-1' } });
    await router.isReady();
  });

  it('fetches portfolio details on mount and displays them', async () => {
    // Arrange
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve(mockPortfolio) });
    const wrapper = mount(PortfolioDetailsView, { global: { plugins: [pinia, router] } });
    const store = usePortfolioStore();

    // Assert: fetch was called on mount
    expect(store.fetchPortfolioById).toHaveBeenCalledWith('pf-1');
    
    // Arrange: update store state to simulate fetch completion
    store.currentPortfolio = mockPortfolio;
    await wrapper.vm.$nextTick();

    // Assert: details are rendered
    expect(wrapper.text()).toContain('Detailed Portfolio');
    expect(wrapper.text()).toContain('A test portfolio for details.');
    expect(wrapper.text()).toContain('Total Cash: $50,000.00');
    expect(wrapper.findComponent({ name: 'VCard', text: 'Holdings' }).exists()).toBe(true);
  });

  it('navigates to edit view on edit button click', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve(mockPortfolio) });
    const wrapper = mount(PortfolioDetailsView, { global: { plugins: [pinia, router] } });
    const push = vi.spyOn(router, 'push');
    usePortfolioStore().currentPortfolio = mockPortfolio; // Set state
    await wrapper.vm.$nextTick();

    await wrapper.find('button.v-btn[color="primary"]').trigger('click');

    expect(push).toHaveBeenCalledWith({ name: 'portfolio-edit', params: { id: 'pf-1' } });
  });

  it('opens confirmation dialog and deletes on confirm', async () => {
    // Arrange
    mockFetch.mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(mockPortfolio) });
    const wrapper = mount(PortfolioDetailsView, { global: { plugins: [pinia, router] } });
    const store = usePortfolioStore();
    const push = vi.spyOn(router, 'push');
    store.currentPortfolio = mockPortfolio;
    await wrapper.vm.$nextTick();

    // Act 1: Open dialog
    await wrapper.find('button.v-btn[color="error"]').trigger('click');
    await wrapper.vm.$nextTick();

    // Assert 1: Dialog is visible
    const dialog = wrapper.findComponent({ name: 'ConfirmationDialog' });
    expect(dialog.exists()).toBe(true);
    expect(dialog.text()).toContain("delete the portfolio 'Detailed Portfolio'");

    // Arrange 2: Mock the DELETE fetch call and subsequent GET for list refresh
    mockFetch.mockResolvedValueOnce({ ok: true, status: 204, json: () => Promise.resolve() }); // For DELETE
    mockFetch.mockResolvedValueOnce({ ok: true, json: () => Promise.resolve([]) }); // For list refresh

    // Act 2: Confirm deletion
    await dialog.vm.$emit('confirm');

    // Assert 2: Store action was called and router navigates away
    expect(store.deletePortfolio).toHaveBeenCalledWith('pf-1');
    await wrapper.vm.$nextTick();
    expect(push).toHaveBeenCalledWith({ name: 'dashboard' });
  });
});