import { beforeEach, describe, it, expect, vi } from 'vitest';
import { createPinia, setActivePinia } from 'pinia';
import { createSentinelRouter } from '@/router';
import { useAuthStore } from '@/stores/auth';
import { onAuthStateChanged } from 'firebase/auth';

// This is the only mock we need.
vi.mock('firebase/auth', () => ({
  getAuth: vi.fn(),
  onAuthStateChanged: vi.fn(),
  signInWithEmailAndPassword: vi.fn(),
  signOut: vi.fn(),
}));

describe('Auth Router Guards', () => {
  let router: ReturnType<typeof createSentinelRouter>;
  const onAuthStateChangedMock = onAuthStateChanged as vi.Mock;

  beforeEach(() => {
    vi.clearAllMocks();
    setActivePinia(createPinia());
    router = createSentinelRouter();
  });

  it('redirects unauthenticated user from protected route to login', async () => {
    // ARRANGE: Firebase reports the user is logged out.
    onAuthStateChangedMock.mockImplementation((auth, callback) => {
      callback(null);
    });

    // ACT: Try to navigate to a protected route.
    await router.push({ name: 'dashboard' });
    await router.isReady();

    // ASSERT: We ended up on the login page.
    expect(router.currentRoute.value.name).toBe('login');
  });

  it('allows unauthenticated user to access public home page', async () => {
    onAuthStateChangedMock.mockImplementation((auth, callback) => {
      callback(null);
    });

    await router.push({ name: 'home' });
    await router.isReady();

    expect(router.currentRoute.value.name).toBe('home');
  });

  it('allows unauthenticated user to access login page', async () => {
    onAuthStateChangedMock.mockImplementation((auth, callback) => {
      callback(null);
    });

    await router.push({ name: 'login' });
    await router.isReady();

    expect(router.currentRoute.value.name).toBe('login');
  });

  it('redirects authenticated user from login page to dashboard', async () => {
    // ARRANGE: Firebase reports the user is logged in.
    const mockUser = { uid: '123', email: 'test@test.com' };
    onAuthStateChangedMock.mockImplementation((auth, callback) => {
      callback(mockUser);
    });

    // ACT: Try to navigate to the login page while authenticated.
    await router.push({ name: 'login' });
    await router.isReady();

    // ASSERT: We were redirected to the dashboard.
    expect(router.currentRoute.value.name).toBe('dashboard');
  });

  it('redirects authenticated user from home page to dashboard', async () => {
    // ARRANGE: Firebase reports the user is logged in.
    const mockUser = { uid: '123', email: 'test@test.com' };
    onAuthStateChangedMock.mockImplementation((auth, callback) => {
      callback(mockUser);
    });

    // ACT: Try to navigate to the home page while authenticated.
    await router.push({ name: 'home' });
    await router.isReady();

    // ASSERT: We were redirected to the dashboard.
    expect(router.currentRoute.value.name).toBe('dashboard');
});

  it('allows authenticated user to access protected dashboard', async () => {
    // ARRANGE: Firebase reports the user is logged in.
    const mockUser = { uid: '123', email: 'test@test.com' };
    onAuthStateChangedMock.mockImplementation((auth, callback) => {
      callback(mockUser);
    });

    await router.push({ name: 'dashboard' });
    await router.isReady();

    expect(router.currentRoute.value.name).toBe('dashboard');
  });
});

