// frontend/tests/stores/userSettings.spec.ts
// This is a high-fidelity test for the userSettings Pinia store.
// It uses real service instances and mocks only the global `fetch` function.
// References: docs/testing_strategy.md (Section 4.2)

import { setActivePinia, createPinia } from 'pinia';
import { useUserSettingsStore } from '@/stores/userSettings';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { auth } from '@/plugins/firebase'; // We will mock this
import type { User, PortfolioSummary, UpdateUserSettingsRequest } from '@/api/models';

// Mock the Firebase auth module
vi.mock('@/plugins/firebase', () => ({
  auth: {
    currentUser: {
      getIdToken: vi.fn(),
    },
  },
}));

// Mock the global fetch function
const mockFetch = vi.fn();
global.fetch = mockFetch;

// --- Mock Data ---
const mockUser: User = {
  uid: 'test-uid',
  username: 'test-user',
  email: 'test@example.com',
  defaultPortfolioId: 'pf-1',
  subscriptionStatus: 'FREE',
  notificationPreferences: ['EMAIL'],
  createdAt: new Date().toISOString(),
  modifiedAt: new Date().toISOString(),
};

const mockPortfolios: PortfolioSummary[] = [
  { portfolioId: 'pf-1', name: 'My Portfolio', currentValue: 1000 },
];

// --- Test Suite ---
describe('User Settings Store (High-Fidelity)', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    mockFetch.mockClear();
    vi.clearAllMocks();
  });

  it('should fetch user settings and portfolios successfully', async () => {
    const store = useUserSettingsStore();
    
    // Arrange: Mock the auth token and the two fetch responses
    vi.mocked(auth.currentUser?.getIdToken).mockResolvedValue('mock-token');
    mockFetch
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(mockUser) }) // For settings
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(mockPortfolios) }); // For portfolios

    // Act
    await store.fetchUserSettings();

    // Assert
    expect(store.isLoading).toBe(false);
    expect(store.error).toBe(null);
    expect(store.userSettings).toEqual(mockUser);
    expect(store.portfolios).toEqual(mockPortfolios);
    expect(auth.currentUser?.getIdToken).toHaveBeenCalledTimes(2); // Called by each service
    expect(mockFetch).toHaveBeenCalledTimes(2);
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/users/me/settings'),
      expect.objectContaining({ method: 'GET' })
    );
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/users/me/portfolios'),
      expect.objectContaining({ method: 'GET' })
    );
  });

  it('should handle error when fetching user settings', async () => {
    const store = useUserSettingsStore();
    const errorMessage = 'Network error';
    
    // Arrange: Mock the auth token and a failed fetch response
    vi.mocked(auth.currentUser?.getIdToken).mockResolvedValue('mock-token');
    mockFetch.mockResolvedValue({ ok: false, status: 500, json: () => Promise.resolve({ detail: errorMessage }) });

    // Act
    await store.fetchUserSettings();

    // Assert
    expect(store.isLoading).toBe(false);
    expect(store.error).toBe(errorMessage);
    expect(store.userSettings).toBe(null);
    expect(store.portfolios).toEqual([]);
  });

  it('should update user settings successfully', async () => {
    const store = useUserSettingsStore();
    const updateRequest: UpdateUserSettingsRequest = {
      defaultPortfolioId: 'portfolio2',
      notificationPreferences: ['EMAIL', 'PUSH'],
    };
    const updatedUserResponse: User = { ...mockUser, ...updateRequest };
    
    // Arrange: Mock the auth token and the successful PUT response
    vi.mocked(auth.currentUser?.getIdToken).mockResolvedValue('mock-token');
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve(updatedUserResponse) });
    
    // Act
    await store.updateUserSettings(updateRequest);

    // Assert
    expect(store.isLoading).toBe(false);
    expect(store.error).toBe(null);
    expect(store.userSettings).toEqual(updatedUserResponse);
    expect(mockFetch).toHaveBeenCalledTimes(1);
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/users/me/settings'),
      expect.objectContaining({
        method: 'PUT',
        body: JSON.stringify(updateRequest),
      })
    );
  });
});