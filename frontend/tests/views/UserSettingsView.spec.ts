// frontend/tests/unit/views/UserSettingsView.spec.ts
import { mount, VueWrapper } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createTestingPinia, type TestingPinia } from '@pinia/testing';
import { createSentinelRouter } from '@/router';
import type { Router } from 'vue-router';

import UserSettingsView from '@/views/UserSettingsView.vue';

import { useUserSettingsStore } from '@/stores/userSettings';
import { useAuthStore } from '@/stores/auth';

// This test is a high-fidelity integration test for the UserSettingsView.
// It uses a real router instance and real child components to verify the
// view's behavior in a realistic environment.
describe('UserSettingsView.vue', () => {
  let wrapper: VueWrapper<any>;
  let pinia: TestingPinia;
  let userSettingsStore: ReturnType<typeof useUserSettingsStore>;
  let authStore: ReturnType<typeof useAuthStore>;
  let router: Router;

  const mockSettings = {
    uid: 'test-user',
    username: 'Test User',
    email: 'test@example.com',
    defaultPortfolioId: 'portfolio1',
    notificationPreferences: ['EMAIL'],
  };

  const mockPortfolios = [
    { portfolioId: 'portfolio1', name: 'Portfolio 1', defaultCurrency: 'USD' },
    { portfolioId: 'portfolio2', name: 'Portfolio 2', defaultCurrency: 'EUR' },
  ];

  const mountComponent = () => {
    return mount(UserSettingsView, {
      global: {
        plugins: [pinia, router],
        // Per your suggestion, we are not stubbing any child components.
        // This makes the test a higher-fidelity integration test that verifies
        // the view and its real children work together correctly.
        stubs: {},
      },
    });
  };

  beforeEach(async () => {
    vi.clearAllMocks();

    // Initialize pinia and router here, before each test
    pinia = createTestingPinia({
      createSpy: vi.fn,
    });
    router = createSentinelRouter();

    userSettingsStore = useUserSettingsStore(pinia);
    authStore = useAuthStore(pinia);

    // With `@pinia/testing`, actions are stubbed by default and don't modify state.
    // We must set state and getters directly to simulate the desired test conditions.
    // Set isAuthenticated to true for all tests in this suite, as this is a protected view.
    authStore.isAuthenticated = true;

    userSettingsStore.fetchUserSettings.mockResolvedValue();
    userSettingsStore.updateUserSettings.mockResolvedValue();
    authStore.logout.mockResolvedValue();

    // We must navigate to the correct route before mounting the component
    // so that StandardLayout can correctly read the route's meta properties.
    await router.push({ name: 'settings' });
    await router.isReady(); // Ensure router is ready after navigation

    // Mount the component after router is ready
    wrapper = mount(UserSettingsView, {
      global: {
        plugins: [pinia, router],
        stubs: {},
      },
    });
    await wrapper.vm.$nextTick(); // Wait for initial render and watchers
  });

  it('should fetch user settings when mounted', async () => {
    expect(userSettingsStore.fetchUserSettings).toHaveBeenCalledOnce();
  });

  it('should show loading indicator when store is loading', async () => {
    // Directly set the store state and wait for the component to react.
    userSettingsStore.isLoading = true;
    await wrapper.vm.$nextTick();

    expect(wrapper.findComponent({ name: 'VProgressLinear' }).exists()).toBe(true);
    expect(wrapper.findComponent({ name: 'SettingsForm' }).exists()).toBe(false);
  });

  it('should display error message if store has an error', async () => {
    const error = 'Failed to load settings';
    // Directly set the store state and wait for the component to react.
    userSettingsStore.error = error;
    userSettingsStore.isLoading = false;
    await wrapper.vm.$nextTick();

    const errorMessage = wrapper.findComponent({ name: 'ErrorMessage' });
    expect(errorMessage.exists()).toBe(true);
    expect(errorMessage.props('message')).toBe(error);
    expect(wrapper.findComponent({ name: 'VProgressLinear' }).exists()).toBe(false);
  });

  describe('when data is loaded successfully', () => {
    beforeEach(async () => {
      // The wrapper is already mounted and auth state is set in the outer beforeEach.
      // Directly set the store state to simulate a successful data load.
      userSettingsStore.userSettings = mockSettings;
      userSettingsStore.portfolios = mockPortfolios;
      userSettingsStore.isLoading = false;
      // Allow the watcher in the component to react to the store change
      await wrapper.vm.$nextTick();
    });

    it('should display user settings correctly', () => {
      const defaultPortfolioSelect = wrapper.findComponent({ name: 'SelectField' });
      expect(defaultPortfolioSelect.exists()).toBe(true);
      expect(defaultPortfolioSelect.props('modelValue')).toBe(mockSettings.defaultPortfolioId);
      expect(defaultPortfolioSelect.props('items')).toEqual(mockPortfolios);

      const notificationSelect = wrapper.findComponent({ name: 'MultiSelect' });
      expect(notificationSelect.exists()).toBe(true);
      expect(notificationSelect.props('modelValue')).toEqual(mockSettings.notificationPreferences);
    });

    it('should call updateUserSettings and navigate back on save', async () => {
      // GIVEN the form is loaded and the user changes a value
      const backSpy = vi.spyOn(router, 'back');
      wrapper.vm.localUserSettings.defaultPortfolioId = 'portfolio2';
      await wrapper.vm.$nextTick();

      // WHEN the user clicks save
      const formActions = wrapper.findComponent({ name: 'FormActions' });
      expect(formActions.exists()).toBe(true);
      await formActions.vm.$emit('USER_CLICKS_SAVE');

      // THEN the store should be updated with the new values
      expect(userSettingsStore.updateUserSettings).toHaveBeenCalledOnce();
      expect(userSettingsStore.updateUserSettings).toHaveBeenCalledWith({
        defaultPortfolioId: 'portfolio2',
        notificationPreferences: mockSettings.notificationPreferences,
      });

      // AND the user should be navigated back
      await wrapper.vm.$nextTick();
      expect(backSpy).toHaveBeenCalledOnce();
    });

    it('should navigate back on cancel', async () => {
      const backSpy = vi.spyOn(router, 'back');
      const formActions = wrapper.findComponent({ name: 'FormActions' });
      expect(formActions.exists()).toBe(true);
      await formActions.vm.$emit('USER_CLICKS_CANCEL');
      expect(backSpy).toHaveBeenCalledOnce();
    });
  });
});