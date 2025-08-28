// frontend/src/stores/userSettings.ts
// This store manages user-specific settings, including default portfolio and notification preferences.
// It interacts with the backend API for fetching and updating these settings.
// References: product_spec.md Chapter 9, docs/specs/views_spec.yaml (VIEW_USER_SETTINGS), docs/specs/ui_flows_spec.yaml (FLOW_MANAGE_USER_SETTINGS)

import { defineStore } from 'pinia';
import { ref } from 'vue';
import { auth } from '@/plugins/firebase'; // Assuming firebase.ts exports auth
import { API_BASE_URL } from '@/config'; // Assuming config.ts defines API_BASE_URL

// Define interfaces for the data models
interface UserSettings {
  userId: string;
  email: string;
  defaultPortfolioId: string | null;
  notificationPreferences: ('EMAIL' | 'PUSH')[];
  createdAt: string;
  modifiedAt: string;
}

interface PortfolioSummary {
  portfolioId: string;
  name: string;
}

export const useUserSettingsStore = defineStore('userSettings', () => {
  const userSettings = ref<UserSettings | null>(null);
  const portfolios = ref<PortfolioSummary[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  /**
   * Fetches the user's settings and their portfolios from the backend.
   * References: product_spec.md Section 9.1.1 (S_1000)
   */
  const fetchUserSettings = async () => {
    isLoading.value = true;
    error.value = null;
    try {
      const token = await auth.currentUser?.getIdToken();
      if (!token) {
        throw new Error('Authentication token not found.');
      }

      // Fetch user settings
      const settingsResponse = await fetch(`${API_BASE_URL}/users/me/settings`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!settingsResponse.ok) {
        const errorData = await settingsResponse.json();
        throw new Error(errorData.message || 'Failed to fetch user settings.');
      }
      userSettings.value = await settingsResponse.json();

      // Fetch portfolios for the dropdown
      const portfoliosResponse = await fetch(`${API_BASE_URL}/users/me/portfolios`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!portfoliosResponse.ok) {
        const errorData = await portfoliosResponse.json();
        throw new Error(errorData.message || 'Failed to fetch portfolios.');
      }
      portfolios.value = (await portfoliosResponse.json()).map((p: any) => ({
        portfolioId: p.portfolioId,
        name: p.name,
      }));

    } catch (err: any) {
      console.error('Error fetching user settings:', err);
      error.value = err.message || 'An unexpected error occurred.';
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Updates the user's settings on the backend.
   * References: product_spec.md Section 9.1.2 (S_2000)
   * @param updatedSettings The partial settings object to update.
   */
  const updateUserSettings = async (updatedSettings: Partial<UserSettings>) => {
    isLoading.value = true;
    error.value = null;
    try {
      const token = await auth.currentUser?.getIdToken();
      if (!token) {
        throw new Error('Authentication token not found.');
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

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to update user settings.');
      }

      // Update local state with the new settings
      userSettings.value = { ...userSettings.value, ...updatedSettings } as UserSettings;

    } catch (err: any) {
      console.error('Error updating user settings:', err);
      error.value = err.message || 'An unexpected error occurred.';
    } finally {
      isLoading.value = false;
    }
  };

  return {
    userSettings,
    portfolios,
    isLoading,
    error,
    fetchUserSettings,
    updateUserSettings,
  };
});
