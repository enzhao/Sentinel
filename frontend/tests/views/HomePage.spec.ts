import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import HomePage from '@/views/HomePage.vue';
 
// Mock the entire Firebase SDK modules. This prevents the real SDK from
// trying to initialize with missing environment variables, which would cause
// an 'auth/invalid-api-key' error.
vi.mock('firebase/app', () => ({
  initializeApp: vi.fn(() => ({})),
}));
vi.mock('firebase/auth', () => ({
  getAuth: vi.fn(() => ({})),
  onAuthStateChanged: vi.fn(),
}));
vi.mock('firebase/firestore', () => ({
  getFirestore: vi.fn(() => ({})),
  // Add other Firestore functions if they are directly used in the store or component
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
