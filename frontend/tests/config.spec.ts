// frontend/tests/config.spec.ts
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
    const { API_BASE_URL } = await import('@/config');

    // Assert: Check if the imported constant has the mocked value.
    expect(API_BASE_URL).toBe(testApiUrl);

    // Cleanup: Restore original environment variables.
    vi.unstubAllEnvs();
  });

  it('should use the default proxy path when VITE_API_URL is not set', async () => {
    // Arrange: To test the fallback behavior, we must ensure the environment
    // variable is a falsy value. We stub it as an empty string, which is
    // a more robust approach than assuming it's undefined in the test runner's environment.
    vi.stubEnv('VITE_API_URL', '');

    // Act: Dynamically import the module.
    const { API_BASE_URL } = await import('@/config');

    // Assert: Check if the constant falls back to the default value.
    expect(API_BASE_URL).toBe('/api');

    // Cleanup
    vi.unstubAllEnvs();
  });
});
