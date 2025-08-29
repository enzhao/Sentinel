/// <reference types="vitest/globals" />
import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createPinia, setActivePinia } from 'pinia';
import { createSentinelRouter } from '@/router';
import type { Router } from 'vue-router';
import HomePage from '@/views/HomePage.vue';

// Partially mock 'firebase/auth'. This is crucial. We use the real module
// so that functions like `connectAuthEmulator` (called by `src/plugins/firebase.ts`)
// are available, but we replace `onAuthStateChanged` with a mock we can control
// to prevent tests from hanging during router initialization.
vi.mock('firebase/auth', async (importActual) => {
  const actual = await importActual<typeof import('firebase/auth')>();
  return {
    ...actual,
    onAuthStateChanged: vi.fn((auth, callback) => {
      // Default to unauthenticated for the public home page tests
      callback(null);
      return vi.fn(); // Return a mock unsubscribe function
    }),
  };
});

describe('HomePage.vue', () => {
  let router: Router;

  beforeEach(() => {
    setActivePinia(createPinia());
    router = createSentinelRouter();
  });

  it('renders all sections of the homepage', async () => {
    const wrapper = mount(HomePage, {
      global: {
        plugins: [router],
        // Use real child components for a high-fidelity test
        stubs: {},
      },
    });
    await router.isReady();

    // Verify that all the main marketing sections are present on the page
    expect(wrapper.findComponent({ name: 'HeroSection' }).exists()).toBe(true);
    expect(wrapper.findComponent({ name: 'KeyFeaturesSection' }).exists()).toBe(true);
    expect(wrapper.findComponent({ name: 'ProblemSolutionSection' }).exists()).toBe(true);
    expect(wrapper.findComponent({ name: 'TargetAudienceSection' }).exists()).toBe(true);
  });

  it('navigates to login when "Get Started" is clicked', async () => {
    const wrapper = mount(HomePage, {
      global: {
        plugins: [router],
      },
    });
    await router.isReady();

    const push = vi.spyOn(router, 'push');
    const heroSection = wrapper.findComponent({ name: 'HeroSection' });
    
    // Simulate the event emitted by the HeroSection component
    await heroSection.vm.$emit('USER_CLICKS_GET_STARTED');

    expect(push).toHaveBeenCalledWith({ name: 'login' });
  });
});