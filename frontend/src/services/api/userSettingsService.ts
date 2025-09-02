// frontend/src/services/api/userSettingsService.ts
// This service handles all API interactions related to user settings.

import { apiService } from '../apiService';
import type { User, UpdateUserSettingsRequest } from '@/api/models';

/**
 * Fetches the current user's settings.
 * Reference: product_spec.md#9.3.2 (US_2000)
 */
export const getUserSettings = (): Promise<User> => {
  return apiService.get<User>('/users/me/settings');
};

/**
 * Updates the current user's settings.
 * Reference: product_spec.md#9.3.3 (US_3000)
 */
export const updateUserSettings = (settings: UpdateUserSettingsRequest): Promise<User> => {
  return apiService.put<User>('/users/me/settings', settings);
};