// frontend/tests/unit/config.spec.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('config', () => {
  beforeEach(() => {
    // Reset modules before each test to clear the module cache. This is
    // crucial for re-evaluating the config file under different env conditions.
    vi.resetModules();
  });

  it('should use the VITE_API_URL from environment variables when it is set', async () => {
    // Arrange: Set a mock value for the environment variable.
    const testApiUrl = 'https://api.example.com';
    vi.stubEnv('VITE_API_URL', testApiUrl);

    // Act: Dynamically import the module to apply the mocked environment variable.
    // The path is updated to point from `tests/unit` to `src`.
    const { API_BASE_URL } = await import('@/config');

    // Assert: Check if the imported constant has the mocked value.
    expect(API_BASE_URL).toBe(testApiUrl);

    // Cleanup: Restore original environment variables.
    vi.unstubAllEnvs();
  });

  it('should use the default localhost URL when VITE_API_URL is not set', async () => {
    // Act: Dynamically import the module. No env var is stubbed, so it will be undefined.
    const { API_BASE_URL } = await import('@/config');

    // Assert: Check if the constant falls back to the default value.
    expect(API_BASE_URL).toBe('http://127.0.0.1:8000');
  });
});
