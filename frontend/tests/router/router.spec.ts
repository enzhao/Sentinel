import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createPinia, setActivePinia } from 'pinia';
import { createSentinelRouter } from '@/router';
import { onAuthStateChanged } from 'firebase/auth';

// Partially mock 'firebase/auth'. This is crucial. We use the real module
// so that functions like `connectAuthEmulator` (called by `src/plugins/firebase.ts`)
// are available, but we replace `onAuthStateChanged` with a mock we can control
// for testing the router guards. This avoids the 'connectAuthEmulator is not defined' error.
// We also provide a default implementation that calls the callback with `null`. This
// prevents hangs caused by module-level side effects in `@/router/index.ts` which
// creates a router instance on import, before our tests can configure the mock.
vi.mock('firebase/auth', async (importActual) => {
  const actual = await importActual<typeof import('firebase/auth')>();
  return {
    ...actual,
    onAuthStateChanged: vi.fn((auth, callback) => {
      callback(null); // Default to "not logged in"
      return vi.fn(); // Return a mock unsubscribe function
    }),
  };
});

describe('Auth Router Guards', () => {
  // This mock needs to be dynamically imported after vi.mock has been set up.
  let onAuthStateChanged: vi.Mock;

  beforeEach(async () => {
    vi.clearAllMocks();
    setActivePinia(createPinia());
    onAuthStateChanged = (await import('firebase/auth')).onAuthStateChanged as vi.Mock;
  });

  it('redirects unauthenticated user from protected route to login', async () => {
    // ARRANGE: Firebase reports the user is logged out.
    onAuthStateChanged.mockImplementation((auth, callback) => {
      callback(null);
      return vi.fn(); // Return an unsubscribe function
    });

    const router = createSentinelRouter();

    // ACT: Try to navigate to a protected route.
    await router.push({ name: 'dashboard' });
    await router.isReady();

    // ASSERT: We ended up on the login page.
    expect(router.currentRoute.value.name).toBe('login');
  });

  it('allows unauthenticated user to access public home page', async () => {
    // ARRANGE
    onAuthStateChanged.mockImplementation((auth, callback) => {
      callback(null);
      return vi.fn();
    });

    // ACT
    const router = createSentinelRouter();
    await router.push({ name: 'home' });
    await router.isReady();

    // ASSERT
    expect(router.currentRoute.value.name).toBe('home');
  });

  it('allows unauthenticated user to access login page', async () => {
    // ARRANGE
    onAuthStateChanged.mockImplementation((auth, callback) => {
      callback(null);
      return vi.fn();
    });

    // ACT
    const router = createSentinelRouter();
    await router.push({ name: 'login' });
    await router.isReady();

    // ASSERT
    expect(router.currentRoute.value.name).toBe('login');
  });

  it('redirects authenticated user from login page to dashboard', async () => {
    // ARRANGE: Firebase reports the user is logged in.
    const mockUser = { uid: '123', email: 'test@test.com' };
    onAuthStateChanged.mockImplementation((auth, callback) => {
      callback(mockUser);
      return vi.fn();
    });

    const router = createSentinelRouter();

    // ACT: Try to navigate to the login page while authenticated.
    await router.push({ name: 'login' });
    await router.isReady();

    // ASSERT: We were redirected to the dashboard.
    expect(router.currentRoute.value.name).toBe('dashboard');
  });

  it('allows authenticated user to access home page', async () => {
    console.log('[DIAGNOSTIC] Test: allows authenticated user to access home page');
    // ARRANGE: Firebase reports the user is logged in.
    const mockUser = { uid: '123', email: 'test@test.com' };
    onAuthStateChanged.mockImplementation((auth, callback) => {
      console.log('[DIAGNOSTIC] onAuthStateChanged mock called (authenticated)');
      callback(mockUser);
      return vi.fn();
    });

    const router = createSentinelRouter();

    // ACT: As you suggested, we will trigger a new navigation to get the router
    // out of its initial state, which is causing the timeout.
    // 1. First, navigate to a different, known-good route to stabilize it.
    await router.push({ name: 'dashboard' });
    // 2. Now, navigate to the 'home' route to test the actual guard behavior.
    await router.push({ name: 'home' });

    // ASSERT: We were NOT redirected and are on the home page.
    expect(router.currentRoute.value.name).toBe('home');
  });

  it('allows authenticated user to access protected dashboard', async () => {
    // ARRANGE: Firebase reports the user is logged in.
    const mockUser = { uid: '123', email: 'test@test.com' };
    onAuthStateChanged.mockImplementation((auth, callback) => {
      callback(mockUser);
      return vi.fn();
    });

    const router = createSentinelRouter();
    await router.push({ name: 'dashboard' });
    await router.isReady();

    expect(router.currentRoute.value.name).toBe('dashboard');
  });
});
