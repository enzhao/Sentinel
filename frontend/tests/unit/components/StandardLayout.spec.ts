import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createWebHistory } from 'vue-router';
import StandardLayout from '@/components/StandardLayout.vue';
import { useAuthStore } from '@/stores/auth';
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
  props: ['title', 'actions'],
  emits: ['USER_CLICKS_LOGIN', 'USER_CLICKS_LOGOUT'],
};

describe('StandardLayout.vue', () => {
  const router = createRouter({
    history: createWebHistory(),
    routes: [
      { path: '/login', name: 'login', component: {} },
    ],
  });
  const onAuthStateChangedMock = onAuthStateChanged as vi.Mock;

  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  const mountComponent = () => {
    return mount(StandardLayout, {
      global: {
        plugins: [router],
        stubs: { AppBar: AppBarStub },
      },
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
    const wrapper = mountComponent();
    await nextTick();
    const appBar = wrapper.findComponent(AppBarStub);

    // ASSERT
    expect(appBar.props('actions')).toEqual([{ label: 'Login', event: 'USER_CLICKS_LOGIN' }]);
  });

  it('computes logout action when user is authenticated', async () => {
    // ARRANGE: Firebase reports the user is logged in
    const mockUser = { uid: '123', email: 'test@test.com' };
    onAuthStateChangedMock.mockImplementation((auth, callback) => {
      callback(mockUser);
    });
    const authStore = useAuthStore();
    await authStore.init();

    // ACT
    const wrapper = mountComponent();
    await nextTick();
    const appBar = wrapper.findComponent(AppBarStub);

    // ASSERT
    expect(appBar.props('actions')).toEqual([{ label: 'Logout', event: 'USER_CLICKS_LOGOUT' }]);
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
});

