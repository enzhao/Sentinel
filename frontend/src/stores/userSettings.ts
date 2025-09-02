// frontend/src/stores/userSettings.ts
// This store manages user-specific settings, including default portfolio and notification preferences.
// It interacts with the backend API for fetching and updating these settings.
// References: product_spec.md Chapter 9, docs/specs/views_spec.yaml (VIEW_USER_SETTINGS), docs/specs/ui_flows_spec.yaml (FLOW_MANAGE_USER_SETTINGS)

import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { User, UpdateUserSettingsRequest, PortfolioSummary } from '@/api/models'
import * as userSettingsService from '@/services/api/userSettingsService'
import * as portfolioService from '@/services/api/portfolioService'

export const useUserSettingsStore = defineStore('userSettings', () => {
  const userSettings = ref<User | null>(null);
  const portfolios = ref<PortfolioSummary[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  /**
   * Fetches the user's settings and their portfolios from the backend.
   * References: product_spec.md Section 9.3.2 (US_2000)
   */
  const fetchUserSettings = async () => {
    if (userSettings.value || isLoading.value) return;

    isLoading.value = true;
    error.value = null;
    try {
      console.log('Fetching user settings and portfolios...');
      
      // Use Promise.all to fetch in parallel
      const [settingsResponse, portfoliosResponse] = await Promise.all([
        userSettingsService.getUserSettings(),
        portfolioService.listPortfolios()
      ]);

      userSettings.value = settingsResponse;
      portfolios.value = portfoliosResponse;

      console.log('✅ User settings and portfolios fetched successfully.');
      console.log('User Settings:', userSettings.value);
    } catch (err: unknown) {
      console.error('Error in fetchUserSettings action:', err);
      if (err instanceof Error) {
        error.value = err.message;
      } else {
        error.value = 'An unexpected error occurred.';
      }
      userSettings.value = null;
      portfolios.value = [];
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Updates the user's settings on the backend.
   * References: product_spec.md Section 9.3.3 (US_3000)
   * @param updatedSettings The partial settings object to update.
   */
  const updateUserSettings = async (updatedSettings: UpdateUserSettingsRequest) => {
    isLoading.value = true;
    error.value = null;
    try {
      const updatedUser = await userSettingsService.updateUserSettings(updatedSettings);

      // Update local state with the new settings
      userSettings.value = updatedUser;

    } catch (err: unknown) {
      console.error('Error updating user settings:', err);
      if (err instanceof Error) {
        error.value = err.message;
      } else {
        error.value = 'An unexpected error occurred.';
      }
    } finally {
      isLoading.value = false;
    }
  };

  const clearUserSettings = () => {
    userSettings.value = null;
    portfolios.value = [];
  }

  return {
    userSettings,
    portfolios,
    isLoading,
    error,
    fetchUserSettings,
    updateUserSettings,
    clearUserSettings,
  };
});
