/// <reference types="vitest/globals" />
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { nextTick } from 'vue';
import { VApp } from 'vuetify/components';
import LoginForm from '@/views/LoginForm.vue';
import { vuetify } from '~/vitest.setup.ts';
import { signInWithEmailAndPassword } from 'firebase/auth';

// --- CORRECTED MOCK FOR FIREBASE/AUTH (Partial Mock) ---
vi.mock('firebase/app', () => ({
  initializeApp: vi.fn(() => ({})),
}));
vi.mock('firebase/auth', async (importOriginal) => {
  const actual = await importOriginal<typeof import('firebase/auth')>();
  return {
    ...actual, // Keep all original exports
    getAuth: vi.fn(() => ({})), // Override specific functions we need
    signInWithEmailAndPassword: vi.fn(),
    // Provide a dummy onAuthStateChanged to prevent the router guard from crashing
    onAuthStateChanged: vi.fn(), 
  };
});
vi.mock('firebase/firestore', () => ({
  getFirestore: vi.fn(() => ({})),
  // Add other Firestore functions if they are directly used in the store or component
}));

// We are partially mocking vue-router to control its push method
const mockRouterPush = vi.fn();
vi.mock('vue-router', async (importOriginal) => {
  const actual = await importOriginal<typeof import('vue-router')>();
  return {
    ...actual,
    useRouter: vi.fn(() => ({
      push: mockRouterPush,
    })),
  };
});


describe('LoginForm.vue', () => {
  let mockSignIn: vi.Mock;

  beforeEach(() => {
    setActivePinia(createPinia());
    mockSignIn = signInWithEmailAndPassword as vi.Mock;
    vi.clearAllMocks();
  });

  const mountComponent = () => {
    return mount(VApp, {
      slots: { default: LoginForm },
      attachTo: document.body,
    });
  };

  it('renders correctly', async () => {
    mountComponent();
    await nextTick();

    expect(document.querySelector('.v-card-title')?.textContent).toBe('Login to Sentinel');
    expect(document.querySelector('input[type="email"]')).not.toBeNull();
    expect(document.querySelector('input[type="password"]')).not.toBeNull();
  });

  it('navigates to home when cancel is clicked', async () => {
    const wrapper = mountComponent();
    await nextTick();
    const loginFormWrapper = wrapper.findComponent(LoginForm);

    await loginFormWrapper.vm.cancelLogin();

    expect(mockRouterPush).toHaveBeenCalledWith('/');
  });

  it('calls signInWithEmailAndPassword and navigates to dashboard on successful login', async () => {
    mockSignIn.mockResolvedValueOnce({});
    const wrapper = mountComponent();
    await nextTick();
    const loginFormWrapper = wrapper.findComponent(LoginForm);

    loginFormWrapper.vm.formState.email = 'test@example.com';
    loginFormWrapper.vm.formState.password = 'password123';

    await loginFormWrapper.vm.submitLogin();

    expect(mockSignIn).toHaveBeenCalledWith(expect.any(Object), 'test@example.com', 'password123');
    expect(mockRouterPush).toHaveBeenCalledWith({ name: 'dashboard' });
  });
});
