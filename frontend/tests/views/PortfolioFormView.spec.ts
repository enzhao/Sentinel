import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createPinia, setActivePinia } from 'pinia';
import { createSentinelRouter } from '@/router';
import PortfolioFormView from '@/views/PortfolioFormView.vue';
import type { Portfolio, PortfolioCreationRequest } from '@/api/models';

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
  name: 'Existing Portfolio',
  description: 'A portfolio to be edited.',
  defaultCurrency: 'USD',
  cashReserve: { totalAmount: 50000, warChestAmount: 10000 },
  ruleSetId: null,
  createdAt: new Date().toISOString(),
  modifiedAt: new Date().toISOString(),
};

describe('PortfolioFormView.vue', () => {
  let router;

  beforeEach(() => {
    vi.resetAllMocks();
    setActivePinia(createPinia());
    router = createSentinelRouter();
  });

  describe('Create Mode', () => {
    beforeEach(async () => {
      await router.push({ name: 'portfolio-create' });
      await router.isReady();
    });

    it('renders the form in create mode', () => {
      const wrapper = mount(PortfolioFormView, { global: { plugins: [router] } });
      expect(wrapper.text()).toContain('Create Portfolio');
      // Check for a default value
      const nameInput = wrapper.find('input[label="Portfolio Name"]');
      expect((nameInput.element as HTMLInputElement).value).toBe('');
    });

    it('submits the creation request and navigates on success', async () => {
      const wrapper = mount(PortfolioFormView, { global: { plugins: [router] } });
      const push = vi.spyOn(router, 'push');

      // Arrange: Mock the POST for creation and the subsequent GET for list refresh
      const newPortfolioData: PortfolioCreationRequest = {
        name: 'My New Creation',
        description: 'A brand new start',
        defaultCurrency: 'EUR',
        cashReserve: { totalAmount: 1000, warChestAmount: 100 },
      };
      mockFetch
        .mockResolvedValueOnce({ ok: true, status: 201, json: () => Promise.resolve({ ...mockPortfolio, ...newPortfolioData }) }) // POST
        .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve([]) }); // GET refresh

      // Act: Fill out the form
      await wrapper.find('input[label="Portfolio Name"]').setValue(newPortfolioData.name);
      await wrapper.find('textarea[label="Description (Optional)"]').setValue(newPortfolioData.description);
      // Note: v-select is complex to test by setting value, we'll trust the model binding
      wrapper.vm.formData.defaultCurrency = newPortfolioData.defaultCurrency;
      await wrapper.find('input[label="Total Cash Reserve"]').setValue(newPortfolioData.cashReserve.totalAmount);
      await wrapper.find('input[label="War Chest Amount"]').setValue(newPortfolioData.cashReserve.warChestAmount);
      
      // Trigger save
      await wrapper.find('button.v-btn[color="primary"]').trigger('click');
      await wrapper.vm.$nextTick(); // Allow promises to resolve

      // Assert
      expect(mockFetch).toHaveBeenCalledTimes(2);
      // Check the POST call
      const fetchCall = mockFetch.mock.calls[0];
      expect(fetchCall[0]).toContain('/api/v1/users/me/portfolios');
      expect(fetchCall[1].method).toBe('POST');
      expect(JSON.parse(fetchCall[1].body)).toEqual(newPortfolioData);

      // Check navigation
      expect(push).toHaveBeenCalledWith({ name: 'dashboard' });
    });
  });

  describe('Edit Mode', () => {
    beforeEach(async () => {
      await router.push({ name: 'portfolio-edit', params: { id: 'pf-1' } });
      await router.isReady();
    });

    it('fetches existing data and populates the form', async () => {
      // Arrange: Mock the initial GET request
      mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve(mockPortfolio) });
      const wrapper = mount(PortfolioFormView, { global: { plugins: [router] } });
      
      // Act: Wait for component to mount and fetch data
      await wrapper.vm.$nextTick(); // Let onMounted run
      await wrapper.vm.$nextTick(); // Let promises resolve
      await wrapper.vm.$nextTick(); // Let state update

      // Assert
      expect(mockFetch).toHaveBeenCalledOnce();
      expect(wrapper.text()).toContain('Edit Portfolio');
      const nameInput = wrapper.find('input[label="Portfolio Name"]');
      expect((nameInput.element as HTMLInputElement).value).toBe('Existing Portfolio');
    });

    it('submits the update request and navigates on success', async () => {
      // Arrange: Mock the initial GET, the PUT for update, and the final GET for refresh
      mockFetch
        .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(mockPortfolio) }) // Initial GET
        .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ ...mockPortfolio, name: 'Updated Name' }) }) // PUT
        .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve([]) }); // GET refresh

      const wrapper = mount(PortfolioFormView, { global: { plugins: [router] } });
      const push = vi.spyOn(router, 'push');
      await wrapper.vm.$nextTick();
      await wrapper.vm.$nextTick();

      // Act: Change a value and save
      await wrapper.find('input[label="Portfolio Name"]').setValue('Updated Name');
      await wrapper.find('button.v-btn[color="primary"]').trigger('click');
      await wrapper.vm.$nextTick();

      // Assert
      expect(mockFetch).toHaveBeenCalledTimes(3);
      const putCall = mockFetch.mock.calls[1];
      expect(putCall[0]).toContain('/api/v1/users/me/portfolios/pf-1');
      expect(putCall[1].method).toBe('PUT');
      expect(JSON.parse(putCall[1].body).name).toBe('Updated Name');
      expect(push).toHaveBeenCalledWith({ name: 'dashboard' });
    });
  });
});