import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createPinia, setActivePinia } from 'pinia';
import { useAuthStore } from '@/stores/auth';
import { signOut, signInWithEmailAndPassword } from 'firebase/auth';

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

  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks(); // Reset mocks before each test
  });

  describe('logout', () => {
    it('calls signOut and returns true on success', async () => {
      // ARRANGE: Simulate a successful sign-out
      const authStore = useAuthStore();
      mockSignOut.mockResolvedValue(undefined);

      // ACT: Call the logout action
      const result = await authStore.logout();

      // ASSERT: Check that signOut was called and the action returned true.
      // Navigation is handled by the component that calls this action.
      expect(mockSignOut).toHaveBeenCalled();
      expect(result).toBe(true);
    });

    it('returns false on failed logout', async () => {
      // ARRANGE: Simulate a failed sign-out
      const authStore = useAuthStore();
      mockSignOut.mockRejectedValue(new Error('Logout failed'));

      // ACT: Call the logout action
      const result = await authStore.logout();

      // ASSERT: Check that signOut was called and the action returned false
      expect(mockSignOut).toHaveBeenCalled();
      expect(result).toBe(false);
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
