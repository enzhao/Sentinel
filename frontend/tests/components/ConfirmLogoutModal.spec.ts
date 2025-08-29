/// <reference types="vitest/globals" />
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { getAuth, signOut } from 'firebase/auth';
import { nextTick } from 'vue';
import { VApp } from 'vuetify/components';
import ConfirmLogoutModal from '@/components/ConfirmLogoutModal.vue';

// Mock Firebase auth
vi.mock('firebase/auth', () => ({
  getAuth: vi.fn(() => ({})),
  signOut: vi.fn(),
}));

describe('ConfirmLogoutModal.vue', () => {
  let mockSignOut: vi.Mock;

  beforeEach(() => {
    setActivePinia(createPinia());
    mockSignOut = signOut as vi.Mock;
    vi.clearAllMocks();
  });

  // Mounts the component inside the required VApp wrapper.
  const mountComponent = () => {
    const wrapper = mount(VApp, {
      slots: {
        default: ConfirmLogoutModal,
      },
      attachTo: document.body,
    });
    return wrapper;
  };

  it('renders correctly', async () => {
    mountComponent();
    await nextTick();
    await nextTick(); // Add a second tick to ensure JSDOM is queryable

    const title = document.querySelector('.v-card-title');
    const text = document.querySelector('.v-card-text');
    const buttons = document.querySelectorAll('.v-btn');

    expect(title?.textContent).toBe('Confirm Logout');
    expect(text?.textContent?.trim()).toContain('Are you sure you want to log out?');
    expect(buttons[0]?.textContent?.trim()).toBe('Cancel');
    expect(buttons[1]?.textContent?.trim()).toBe('Logout');
  });

  it('emits user-clicks-cancel when cancelLogout method is called', async () => {
    const wrapper = mountComponent();
    await nextTick();
    await nextTick();

    const modalWrapper = wrapper.findComponent(ConfirmLogoutModal);
    
    // Directly call the method on the component instance
    await modalWrapper.vm.cancelLogout();

    expect(modalWrapper.emitted()['user-clicks-cancel']).toBeTruthy();
    expect(mockSignOut).not.toHaveBeenCalled();
    });

    it('calls signOut and emits user-confirms-logout when confirmLogout method is called', async () => {
        mockSignOut.mockResolvedValueOnce({});
        const wrapper = mountComponent();
        await nextTick();
        await nextTick();

        const modalWrapper = wrapper.findComponent(ConfirmLogoutModal);

        // Directly call the method on the component instance
        await modalWrapper.vm.confirmLogout();

        expect(mockSignOut).toHaveBeenCalledWith(expect.any(Object));
        expect(modalWrapper.emitted()['user-confirms-logout']).toBeTruthy();
    });

  it('does not emit user-confirms-logout on failed logout', async () => {
    mockSignOut.mockRejectedValueOnce(new Error('Logout failed'));
    const wrapper = mountComponent();
    await nextTick();
    await nextTick(); // Add a second tick to ensure JSDOM is queryable

    const modalWrapper = wrapper.findComponent(ConfirmLogoutModal);
    const logoutButton = document.querySelectorAll('.v-btn')[1] as HTMLElement;
    logoutButton.click();
    await nextTick();

    expect(mockSignOut).toHaveBeenCalled();
    expect(modalWrapper.emitted()['user-confirms-logout']).toBeFalsy();
  });
});
