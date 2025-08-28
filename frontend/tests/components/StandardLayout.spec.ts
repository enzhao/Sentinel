import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createWebHistory } from 'vue-router';
import StandardLayout from '@/components/StandardLayout.vue';
import { useAuthStore } from '@/stores/auth';
import { useUserSettingsStore } from '@/stores/userSettings';
import { onAuthStateChanged } from 'firebase/auth';
import { nextTick } from 'vue';

// --- We only mock the lowest-level dependency ---
vi.mock('firebase/auth', () => ({
  getAuth: vi.fn(),
  onAuthStateChanged: vi.fn(), // We will control this in each test
  signOut: vi.fn(),
}));

// Mock the AppBar to isolate the layout component
const AppBarStub = {
  name: 'AppBar',
  template: '<div></div>',
  props: ['title', 'actions', 'userMenu', 'leadingAction'],
  emits: ['USER_CLICKS_LOGIN', 'USER_CLICKS_LOGOUT', 'USER_CLICKS_SETTINGS', 'USER_CLICKS_BACK'],
};

describe('StandardLayout.vue', () => {
  const router = createRouter({
    history: createWebHistory(),
    routes: [
      { path: '/', name: 'home', component: {}, meta: { title: 'Sentinel Home' } },
      { path: '/login', name: 'login', component: {} },
      { path: '/settings', name: 'settings', component: {} },
    ],
  });
  const onAuthStateChangedMock = onAuthStateChanged as vi.Mock;

  beforeEach(() => {
    // Reset router to home before each test
    router.push('/');
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  const mountComponent = (options = {}) => {
    return mount(StandardLayout, {
      global: {
        plugins: [router],
        stubs: { AppBar: AppBarStub },
      },
      // Allow passing slots and other options
      ...options,
    });
  };

  it('computes login action when user is not authenticated', async () => {
    // ARRANGE: Firebase reports the user is logged out
    onAuthStateChangedMock.mockImplementation((auth, callback) => {
      callback(null);
    });
    // Initialize the real store, which will use the mock above
    const authStore = useAuthStore();
    await authStore.init();

    // ACT
    await router.isReady();
    const wrapper = mountComponent();
    await nextTick();
    const appBar = wrapper.findComponent(AppBarStub);

    // ASSERT
    expect(appBar.props('actions')).toEqual([{ label: 'Login', event: 'USER_CLICKS_LOGIN' }]);
  });

  it('computes user menu when user is authenticated', async () => {
    // ARRANGE: Firebase reports the user is logged in
    const mockUser = { uid: '123', email: 'test@test.com' };
    onAuthStateChangedMock.mockImplementation((auth, callback) => {
      callback(mockUser);
    });
    const authStore = useAuthStore();
    const userSettingsStore = useUserSettingsStore();
    userSettingsStore.userSettings = { username: 'Test User' };
    await authStore.init();

    // ACT
    await router.isReady();
    const wrapper = mountComponent();
    await nextTick();
    const appBar = wrapper.findComponent(AppBarStub);

    // ASSERT
    expect(appBar.props('actions')).toBeUndefined();
    expect(appBar.props('userMenu')).toEqual({
      username: 'Test User',
      items: [
        { label: 'Settings', event: 'USER_CLICKS_SETTINGS' },
        { label: 'Logout', event: 'USER_CLICKS_LOGOUT' },
      ],
    });
  });

  it('navigates to login page on USER_CLICKS_LOGIN event', async () => {
    const pushSpy = vi.spyOn(router, 'push');
    const wrapper = mountComponent();
    const appBar = wrapper.findComponent(AppBarStub);

    await appBar.vm.$emit('USER_CLICKS_LOGIN');

    expect(pushSpy).toHaveBeenCalledWith({ name: 'login' });
    pushSpy.mockRestore();
  });

  it('calls authStore.logout on USER_CLICKS_LOGOUT event', async () => {
    const authStore = useAuthStore();
    const logoutSpy = vi.spyOn(authStore, 'logout');
    const wrapper = mountComponent();
    const appBar = wrapper.findComponent(AppBarStub);

    await appBar.vm.$emit('USER_CLICKS_LOGOUT');

    expect(logoutSpy).toHaveBeenCalled();
  });

  it('navigates to settings page on USER_CLICKS_SETTINGS event', async () => {
    const pushSpy = vi.spyOn(router, 'push');
    const wrapper = mountComponent();
    const appBar = wrapper.findComponent(AppBarStub);

    await appBar.vm.$emit('USER_CLICKS_SETTINGS');

    expect(pushSpy).toHaveBeenCalledWith({ name: 'settings' });
    pushSpy.mockRestore();
  });

  it('navigates back on USER_CLICKS_BACK event', async () => {
    const backSpy = vi.spyOn(router, 'back');
    const wrapper = mountComponent();
    const appBar = wrapper.findComponent(AppBarStub);

    await appBar.vm.$emit('USER_CLICKS_BACK');

    expect(backSpy).toHaveBeenCalledOnce();
    backSpy.mockRestore();
  });

  it('renders content in the body, fab, and footer slots', () => {
    const wrapper = mountComponent({
      slots: {
        body: '<div class="body-content">Body Content</div>',
        fab: '<button class="fab-button">FAB</button>',
        footer: '<div class="footer-content">Footer Content</div>',
      },
    });

    const bodyContent = wrapper.find('.body-content');
    expect(bodyContent.exists()).toBe(true);
    expect(bodyContent.text()).toBe('Body Content');

    const fabButton = wrapper.find('.fab-button');
    expect(fabButton.exists()).toBe(true);
    expect(fabButton.text()).toBe('FAB');

    const footerContent = wrapper.find('.footer-content');
    expect(footerContent.exists()).toBe(true);
    expect(footerContent.text()).toBe('Footer Content');
  });
});
