// frontend/tests/unit/stores/userSettings.test.ts
// Unit tests for the userSettings Pinia store.
// References: product_spec.md Chapter 9, docs/testing_strategy.md, GEMINI.md

import { setActivePinia, createPinia } from 'pinia';
import { useUserSettingsStore } from '@/stores/userSettings';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { auth } from '@/plugins/firebase'; // Mock Firebase auth

// Mock the Firebase auth module
vi.mock('@/plugins/firebase', () => ({
  auth: {
    currentUser: {
      getIdToken: vi.fn(() => Promise.resolve('mock-token')),
    },
  },
}));

// Mock the global fetch function
const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('userSettings Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    mockFetch.mockClear();
    vi.clearAllMocks();
  });

  it('should fetch user settings and portfolios successfully', async () => {
    const store = useUserSettingsStore();

    const mockUserSettings = {
      userId: 'user123',
      email: 'test@example.com',
      defaultPortfolioId: 'portfolio1',
      notificationPreferences: ['EMAIL'],
      createdAt: '2023-01-01T00:00:00Z',
      modifiedAt: '2023-01-01T00:00:00Z',
    };

    const mockPortfolios = [
      { portfolioId: 'portfolio1', name: 'My First Portfolio' },
      { portfolioId: 'portfolio2', name: 'Investment Fund' },
    ];

    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockUserSettings),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockPortfolios),
      });

    await store.fetchUserSettings();

    expect(store.isLoading).toBe(false);
    expect(store.error).toBeNull();
    expect(store.userSettings).toEqual(mockUserSettings);
    expect(store.portfolios).toEqual(mockPortfolios);
    expect(auth.currentUser?.getIdToken).toHaveBeenCalled();
    expect(mockFetch).toHaveBeenCalledTimes(2);
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/users/me/settings'),
      expect.any(Object)
    );
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/users/me/portfolios'),
      expect.any(Object)
    );
  });

  it('should handle error when fetching user settings', async () => {
    const store = useUserSettingsStore();

    mockFetch.mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve({ message: 'Network error' }),
    });

    await store.fetchUserSettings();

    expect(store.isLoading).toBe(false);
    expect(store.error).toBe('Network error');
    expect(store.userSettings).toBeNull();
    expect(store.portfolios).toEqual([]);
  });

  it('should update user settings successfully', async () => {
    const store = useUserSettingsStore();

    // Initialize user settings first
    store.userSettings = {
      userId: 'user123',
      email: 'test@example.com',
      defaultPortfolioId: 'portfolio1',
      notificationPreferences: ['EMAIL'],
      createdAt: '2023-01-01T00:00:00Z',
      modifiedAt: '2023-01-01T00:00:00Z',
    };

    const updatedData = {
      defaultPortfolioId: 'portfolio2',
      notificationPreferences: ['EMAIL', 'PUSH'],
    };

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ message: 'Settings updated' }),
    });

    await store.updateUserSettings(updatedData);

    expect(store.isLoading).toBe(false);
    expect(store.error).toBeNull();
    expect(store.userSettings?.defaultPortfolioId).toBe('portfolio2');
    expect(store.userSettings?.notificationPreferences).toEqual(['EMAIL', 'PUSH']);
    expect(auth.currentUser?.getIdToken).toHaveBeenCalled();
    expect(mockFetch).toHaveBeenCalledTimes(1);
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/users/me/settings'),
      expect.objectContaining({
        method: 'PUT',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
          'Authorization': 'Bearer mock-token',
          'Idempotency-Key': expect.any(String),
        }),
        body: JSON.stringify(updatedData),
      })
    );
  });

  it('should handle error when updating user settings', async () => {
    const store = useUserSettingsStore();

    // Initialize user settings first
    store.userSettings = {
      userId: 'user123',
      email: 'test@example.com',
      defaultPortfolioId: 'portfolio1',
      notificationPreferences: ['EMAIL'],
      createdAt: '2023-01-01T00:00:00Z',
      modifiedAt: '2023-01-01T00:00:00Z',
    };

    const updatedData = {
      defaultPortfolioId: 'portfolio2',
    };

    mockFetch.mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve({ message: 'Validation error' }),
    });

    await store.updateUserSettings(updatedData);

    expect(store.isLoading).toBe(false);
    expect(store.error).toBe('Validation error');
    // Ensure local state is not updated on error
    expect(store.userSettings?.defaultPortfolioId).toBe('portfolio1');
  });
});
