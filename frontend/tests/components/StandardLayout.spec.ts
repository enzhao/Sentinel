import { mount } from '@vue/test-utils'
import type { Router } from 'vue-router'
import { createPinia, setActivePinia } from 'pinia'
import { describe, it, expect, vi, beforeEach } from 'vitest'

import StandardLayout from '@/components/StandardLayout.vue'
import AppBar from '@/components/AppBar.vue'
import { createSentinelRouter } from '@/router'
import { useAuthStore } from '@/stores/auth'
import { useUserSettingsStore } from '@/stores/userSettings'

// Partially mock 'firebase/auth'. This is the key to preventing the test from hanging.
// We use the real module for connecting to the emulator but replace the problematic
// `onAuthStateChanged` function. This mock immediately invokes the callback to
// simulate the initial auth state check, allowing `authStore.init()` to resolve.
vi.mock('firebase/auth', async (importActual) => {
  const actual = await importActual<typeof import('firebase/auth')>();
  return {
    ...actual,
    onAuthStateChanged: vi.fn((auth, callback) => {
      callback(null); // Simulate initial "not logged in" state
      return vi.fn(); // Return a mock unsubscribe function
    }),
  };
});

describe('StandardLayout.vue', () => {
  // We don't define a global router instance here.
  // A fresh one will be created for each test inside mountComponent.
  let router: Router;
  let authStore: ReturnType<typeof useAuthStore>
  let userSettingsStore: ReturnType<typeof useUserSettingsStore>

  // Helper function to mount the component with a fresh router and Pinia store.
  const mountComponent = async () => {
    router = createSentinelRouter();
    return mount(StandardLayout, {
      global: {
        plugins: [router], // Pinia is active globally via setActivePinia
      },
      slots: {
        body: '<div>Page Content</div>',
      },
    })
  }

  beforeEach(() => {
    // 1. Set up a real Pinia instance and get the stores.
    setActivePinia(createPinia());
    authStore = useAuthStore();
    userSettingsStore = useUserSettingsStore();

    // 2. Mock store actions that make external API calls. We no longer mock
    // `authStore.init` because we have mocked the underlying `onAuthStateChanged`
    // call, making the real `init` function safe to run in tests.
    authStore.logout = vi.fn().mockResolvedValue(true);
    userSettingsStore.fetchUserSettings = vi.fn().mockResolvedValue(undefined);
    userSettingsStore.clearUserSettings = vi.fn();

    // 3. Mock other browser-specific methods.
    window.open = vi.fn()
  })

  describe('for an unauthenticated user', () => {
    beforeEach(async () => {
      // Set the underlying state property. The real store's getters will react to this.
      authStore.user = null

      // Ensure the mock reflects the unauthenticated state for the router guard.
      const { onAuthStateChanged } = await import('firebase/auth');
      vi.mocked(onAuthStateChanged).mockImplementation((auth, callback) => {
        callback(null);
        return vi.fn();
      });
    })

    it('renders the AppBar with correct props for unauthenticated users', async () => {
      const wrapper = await mountComponent();
      await router.push({ name: 'home' });
      await wrapper.vm.$nextTick() // Wait for computed properties to update.

      const appBar = wrapper.findComponent(AppBar)
      expect(appBar.exists()).toBe(true)

      const props = appBar.props()
      // The title comes from the route meta in routes.ts
      expect(props.title).toBe('Sentinel Home')

      // Verify the actions passed to the AppBar.
      const actions = props.actions as any[]
      expect(actions.find((a) => a.label === 'Home')).toBeDefined()
      expect(actions.find((a) => a.label === 'Docs')).toBeDefined()
      expect(actions.find((a) => a.label === 'Login')).toBeDefined()
      expect(actions.find((a) => a.label === 'Dashboard')).toBeUndefined()
      // The AppBar component prop defaults to null if not provided.
      expect(props.userMenu).toBeNull()
    })

    it('navigates to login page when login is clicked', async () => {
      const wrapper = await mountComponent()
      const push = vi.spyOn(router, 'push')
      const appBar = wrapper.findComponent(AppBar)

      await appBar.vm.$emit('USER_CLICKS_LOGIN')
      expect(push).toHaveBeenCalledWith({ name: 'login' })
    })
  })

  describe('for an authenticated user', () => {
    beforeEach(async () => {
      // Set the underlying state for the real stores.
      const mockUser = { uid: 'test-uid', email: 'test@example.com' } as any;
      authStore.user = mockUser

      // Ensure the mock reflects the authenticated state for the router guard.
      const { onAuthStateChanged } = await import('firebase/auth');
      vi.mocked(onAuthStateChanged).mockImplementation((auth, callback) => {
        callback(mockUser);
        return vi.fn();
      });

      userSettingsStore.userSettings = {
        uid: 'test-uid',
        username: 'TestUser',
        email: 'test@example.com',
        defaultPortfolioId: 'pf-1',
        subscriptionStatus: 'FREE',
        notificationPreferences: [],
        createdAt: new Date().toISOString(),
        modifiedAt: new Date().toISOString(),
      }
    })

    it('renders the AppBar with correct props for authenticated users', async () => {
      const wrapper = await mountComponent();
      await router.push({ name: 'home' });
      await wrapper.vm.$nextTick()

      const appBar = wrapper.findComponent(AppBar)
      const props = appBar.props()
      // The title comes from the route meta in routes.ts for the home page.
      expect(props.title).toBe('My Portfolios')

      const actions = props.actions as any[]
      expect(actions.find((a) => a.label === 'Home')).toBeDefined()
      expect(actions.find((a) => a.label === 'Docs')).toBeDefined()
      expect(actions.find((a) => a.label === 'Dashboard')).toBeDefined()
      expect(actions.find((a) => a.label === 'Login')).toBeUndefined()

      expect(props.userMenu).toBeDefined()
      expect(props.userMenu.username).toBe('TestUser')
      expect(props.userMenu.items).toHaveLength(2)
    })

    it('navigates to dashboard when dashboard link is clicked', async () => {
      const wrapper = await mountComponent()
      const push = vi.spyOn(router, 'push')
      const appBar = wrapper.findComponent(AppBar);
      expect(appBar.exists()).toBe(true);
      await appBar.vm.$emit('USER_CLICKS_DASHBOARD');
      expect(push).toHaveBeenCalledWith({ name: 'dashboard' })
    })

    it('opens user docs in a new tab when docs link is clicked', async () => {
      const wrapper = await mountComponent()
      const appBar = wrapper.findComponent(AppBar);
      expect(appBar.exists()).toBe(true);
      await appBar.vm.$emit('USER_CLICKS_DOCS');
      expect(window.open).toHaveBeenCalledWith('/user_docs/', '_blank')
    })

    it('handles logout correctly', async () => {
      const wrapper = await mountComponent()
      const push = vi.spyOn(router, 'push')
      const appBar = wrapper.findComponent(AppBar);
      expect(appBar.exists()).toBe(true);

      await appBar.vm.$emit('USER_CLICKS_LOGOUT');
      await wrapper.vm.$nextTick() // Wait for async logout and navigation to complete.

      expect(authStore.logout).toHaveBeenCalled()
      expect(userSettingsStore.clearUserSettings).toHaveBeenCalled()
      expect(push).toHaveBeenCalledWith({ name: 'home' })
    })

    it('fetches user settings on mount if authenticated', async () => {
      // GIVEN the user is authenticated but settings have not been loaded yet
      userSettingsStore.userSettings = null
      // `authStore.isAuthenticated` is already true from the describe block's beforeEach
      await mountComponent()
      expect(userSettingsStore.fetchUserSettings).toHaveBeenCalled()
    })
  })

  describe('general navigation', () => {
    it('navigates to home page when home link is clicked', async () => {
      const wrapper = await mountComponent()
      const push = vi.spyOn(router, 'push')
      const appBar = wrapper.findComponent(AppBar);
      expect(appBar.exists()).toBe(true);
      await appBar.vm.$emit('USER_CLICKS_HOME');
      expect(push).toHaveBeenCalledWith({ name: 'home' })
    })

    it('navigates back when back button is clicked on a page with a back action', async () => {
      const wrapper = await mountComponent()
      // GIVEN a user is on a page with a back button
      await router.push({ name: 'settings' })
      await router.isReady();
      const backSpy = vi.spyOn(router, 'back')
      await wrapper.vm.$nextTick() // Let computed properties update based on new route

      const appBar = wrapper.findComponent(AppBar)
      expect(appBar.props().leadingAction).toBeDefined()

      // WHEN the back event is emitted
      await appBar.vm.$emit('USER_CLICKS_BACK')

      // THEN the router's back method should have been called
      expect(backSpy).toHaveBeenCalledOnce()
    })
  })
})
