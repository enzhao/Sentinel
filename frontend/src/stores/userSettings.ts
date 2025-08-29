// frontend/src/stores/userSettings.ts
// This store manages user-specific settings, including default portfolio and notification preferences.
// It interacts with the backend API for fetching and updating these settings.
// References: product_spec.md Chapter 9, docs/specs/views_spec.yaml (VIEW_USER_SETTINGS), docs/specs/ui_flows_spec.yaml (FLOW_MANAGE_USER_SETTINGS)

import { defineStore } from 'pinia';
import { ref } from 'vue';
import { auth } from '@/plugins/firebase';
import { API_BASE_URL } from '@/config';
import type { User, UpdateUserSettingsRequest, Portfolio } from '@/api/models';

export const useUserSettingsStore = defineStore('userSettings', () => {
  const userSettings = ref<User | null>(null);
  const portfolios = ref<Portfolio[]>([]);
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
      const token = await auth.currentUser?.getIdToken();
      if (!token) {
        throw new Error('U_E_3101: Authentication token not found.');
      }

      console.log('Fetching user settings and portfolios...');
      const headers = { 'Authorization': `Bearer ${token}` };
      
      // Use Promise.all to fetch in parallel
      const [settingsResponse, portfoliosResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/users/me/settings`, { headers }),
        fetch(`${API_BASE_URL}/users/me/portfolios`, { headers })
      ]);

      const settingsData = await settingsResponse.json();
      const portfoliosData = await portfoliosResponse.json();

      if (!settingsResponse.ok) throw new Error(settingsData.detail || 'Failed to fetch user settings.');
      if (!portfoliosResponse.ok) throw new Error(portfoliosData.detail || 'Failed to fetch portfolios.');
      
      userSettings.value = settingsData as User;
      portfolios.value = portfoliosData as Portfolio[];

      console.log('✅ User settings and portfolios fetched successfully.');
      console.log('User Settings:', userSettings.value);
    } catch (err: any) {
      console.error('Error in fetchUserSettings action:', err);
      error.value = err.message || 'An unexpected error occurred.';
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
      const token = await auth.currentUser?.getIdToken();
      if (!token) {
        throw new Error('U_E_3101: Authentication token not found.');
      }

      const response = await fetch(`${API_BASE_URL}/users/me/settings`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'Idempotency-Key': crypto.randomUUID(), // S_I_2002, S_E_2105
        },
        body: JSON.stringify(updatedSettings),
      });

      const responseData = await response.json();
      if (!response.ok) {
        throw new Error(responseData.detail || 'Failed to update user settings.');
      }

      // Update local state with the new settings
      userSettings.value = responseData as User;

    } catch (err: any) {
      console.error('Error updating user settings:', err);
      error.value = err.message || 'An unexpected error occurred.';
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
