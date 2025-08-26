import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import HomePage from '@/views/HomePage.vue';

// Mock the auth store, as StandardLayout (a child) depends on it
vi.mock('@/stores/auth', () => ({
  useAuthStore: vi.fn(() => ({
    isAuthenticated: false,
  })),
}));

describe('HomePage.vue', () => {
  const mountComponent = () => {
    return mount(HomePage, {
      global: {
        plugins: [],
        // We stub the layout and content sections for a focused unit test
        stubs: {
          StandardLayout: { template: '<div><slot name="body"></slot></div>' },
          MarketDataTicker: true,
          HeroSection: true,
          KeyFeaturesSection: true,
          ProblemSolutionSection: true,
          TargetAudienceSection: true,
        },
      },
    });
  };

  it('renders all of its content sections', () => {
    const wrapper = mountComponent();
    
    // Simply check that the content components are present
    expect(wrapper.findComponent({ name: 'MarketDataTicker' }).exists()).toBe(true);
    expect(wrapper.findComponent({ name: 'HeroSection' }).exists()).toBe(true);
    expect(wrapper.findComponent({ name: 'KeyFeaturesSection' }).exists()).toBe(true);
    expect(wrapper.findComponent({ name: 'ProblemSolutionSection' }).exists()).toBe(true);
    expect(wrapper.findComponent({ name: 'TargetAudienceSection' }).exists()).toBe(true);
  });
});
