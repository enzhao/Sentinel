import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createPinia, setActivePinia } from 'pinia';
import { useAuthStore } from '@/stores/auth';
import { signOut, signInWithEmailAndPassword } from 'firebase/auth';
import router from '@/router';

// Mock the router's push method, which is a dependency of the logout action
vi.mock('@/router', () => ({
  default: {
    push: vi.fn(),
  },
}));

// Mock the Firebase Auth functions that the store actions depend on
vi.mock('firebase/auth', () => ({
  getAuth: vi.fn(),
  onAuthStateChanged: vi.fn(),
  signOut: vi.fn(),
  signInWithEmailAndPassword: vi.fn(),
}));

describe('Auth Store Actions', () => {
  // Helpers to easily access the typed mocks
  const mockSignOut = signOut as vi.Mock;
  const mockSignIn = signInWithEmailAndPassword as vi.Mock;
  const mockRouterPush = router.push as vi.Mock;

  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks(); // Reset mocks before each test
  });

  describe('logout', () => {
    it('redirects to the homepage after a successful logout', async () => {
      // ARRANGE: Simulate a successful sign-out
      const authStore = useAuthStore();
      mockSignOut.mockResolvedValue(undefined);

      // ACT: Call the logout action
      await authStore.logout();

      // ASSERT: Check that signOut was called and the router pushed to 'home'
      expect(mockSignOut).toHaveBeenCalled();
      expect(mockRouterPush).toHaveBeenCalledWith({ name: 'home' });
    });
  });

  describe('login', () => {
    it('returns true on successful login', async () => {
      // ARRANGE: Simulate a successful sign-in
      const authStore = useAuthStore();
      const email = 'test@example.com';
      const password = 'password123';
      mockSignIn.mockResolvedValue({ user: { uid: '123' } });

      // ACT: Call the login action
      const result = await authStore.login(email, password);

      // ASSERT: Check that signIn was called correctly and the action returned true
      expect(mockSignIn).toHaveBeenCalledWith(undefined, email, password);
      expect(result).toBe(true);
    });

    it('throws an error on failed login', async () => {
      // ARRANGE: Simulate a failed sign-in
      const authStore = useAuthStore();
      const email = 'wrong@example.com';
      const password = 'wrongpassword';
      const loginError = new Error('Invalid credentials');
      mockSignIn.mockRejectedValue(loginError);

      // ACT & ASSERT: Check that the login action throws the error from Firebase
      await expect(authStore.login(email, password)).rejects.toThrow(loginError);
      expect(mockSignIn).toHaveBeenCalledWith(undefined, email, password);
    });
  });
});

