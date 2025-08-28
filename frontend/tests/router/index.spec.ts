// frontend/tests/unit/router/index.spec.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createPinia, setActivePinia } from 'pinia';
import { createSentinelRouter } from '@/router';
import { useAuthStore } from '@/stores/auth';
import type { Router } from 'vue-router';

// Mock the entire Firebase SDK modules. This prevents the real SDK from
// trying to initialize with missing environment variables, which would cause
// an 'auth/invalid-api-key' error. This is necessary because this test
// indirectly imports the firebase plugin via the router and auth store.
vi.mock('firebase/app', () => ({
  initializeApp: vi.fn(() => ({})),
}));
vi.mock('firebase/auth', () => ({
  getAuth: vi.fn(() => ({})),
  onAuthStateChanged: vi.fn(),
}));
vi.mock('firebase/firestore', () => ({ getFirestore: vi.fn(() => ({})) }));

// This test verifies the navigation guards in the router instance.
// It uses a real router and a mocked auth store to simulate different user states.
describe('Router Navigation Guards', () => {
  let router: Router;
  let authStore: ReturnType<typeof useAuthStore>;

  beforeEach(() => {
    setActivePinia(createPinia());
    router = createSentinelRouter();
    authStore = useAuthStore();
    // Mock the store's init function to resolve immediately
    authStore.init = vi.fn().mockResolvedValue(undefined);
  });

  it('redirects unauthenticated users from protected routes to login', async () => {
    authStore.setUser(null); // Simulate unauthenticated user

    // Attempt to navigate to a protected route
    await router.push({ name: 'settings' });
    await router.isReady();

    // Assert that the router redirected to the login page
    expect(router.currentRoute.value.name).toBe('login');
  });

  it('allows authenticated users to access protected routes', async () => {
    authStore.setUser({ uid: 'test-uid', email: 'test@example.com' } as any); // Simulate authenticated user

    await router.push({ name: 'settings' });
    await router.isReady();

    expect(router.currentRoute.value.name).toBe('settings');
  });

  it('redirects authenticated users from login page to dashboard', async () => {
    authStore.setUser({ uid: 'test-uid', email: 'test@example.com' } as any); // Simulate authenticated user

    await router.push({ name: 'login' });
    await router.isReady();

    expect(router.currentRoute.value.name).toBe('dashboard');
  });

  it('redirects authenticated users from home page to dashboard', async () => {
    authStore.setUser({ uid: 'test-uid', email: 'test@example.com' } as any); // Simulate authenticated user

    await router.push({ name: 'home' });
    await router.isReady();

    expect(router.currentRoute.value.name).toBe('dashboard');
  });
});