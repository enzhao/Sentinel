import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import HomePage from '@/views/HomePage.vue';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { createRouter, createWebHistory } from 'vue-router';

// Mock the sub-components to avoid deep rendering issues and focus on HomePage's structure
const mockMarketDataTicker = { template: '<div class="mock-market-data-ticker"></div>' };
const mockHeroSection = { template: '<div class="mock-hero-section"></div>' };
const mockKeyFeaturesSection = { template: '<div class="mock-key-features-section"></div>' };
const mockProblemSolutionSection = { template: '<div class="mock-problem-solution-section"></div>' };
const mockTargetAudienceSection = { template: '<div class="mock-target-audience-section"></div>' };

const vuetify = createVuetify({
  components,
  directives,
});

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div></div>' } },
    { path: '/login', component: { template: '<div>Login Page</div>' } },
  ],
});

describe('HomePage.vue', () => {
  it('renders all sections of the homepage', async () => {
    router.push('/');
    await router.isReady();

    const wrapper = mount(HomePage, {
      global: {
        plugins: [vuetify, router],
        stubs: {
          MarketDataTicker: mockMarketDataTicker,
          HeroSection: mockHeroSection,
          KeyFeaturesSection: mockKeyFeaturesSection,
          ProblemSolutionSection: mockProblemSolutionSection,
          TargetAudienceSection: mockTargetAudienceSection,
          // AppBar and StandardLayout are also stubs, but we'll test their presence
          AppBar: { template: '<div class="mock-app-bar"><slot></slot></div>' },
          StandardLayout: { template: '<div class="mock-standard-layout"><slot name="header"></slot><slot name="body"></slot></div>' },
        },
      },
    });

    expect(wrapper.findComponent(mockMarketDataTicker).exists()).toBe(true);
    expect(wrapper.findComponent(mockHeroSection).exists()).toBe(true);
    expect(wrapper.findComponent(mockKeyFeaturesSection).exists()).toBe(true);
    expect(wrapper.findComponent(mockProblemSolutionSection).exists()).toBe(true);
    expect(wrapper.findComponent(mockTargetAudienceSection).exists()).toBe(true);
    expect(wrapper.find('.mock-app-bar').exists()).toBe(true);
    expect(wrapper.find('.mock-standard-layout').exists()).toBe(true);
  });

  it('navigates to login page when login button is clicked', async () => {
    const pushSpy = vi.spyOn(router, 'push');
    router.push('/');
    await router.isReady();

    const wrapper = mount(HomePage, {
      global: {
        plugins: [vuetify, router],
        stubs: {
          MarketDataTicker: mockMarketDataTicker,
          HeroSection: mockHeroSection,
          KeyFeaturesSection: mockKeyFeaturesSection,
          ProblemSolutionSection: mockProblemSolutionSection,
          TargetAudienceSection: mockTargetAudienceSection,
          AppBar: {
            template: '<div class="mock-app-bar"></div>',
            emits: ['USER_CLICKS_LOGIN'],
          },
          StandardLayout: { template: '<div><slot name="header"></slot><slot name="body"></slot></div>' },
        },
      },
    });

    // Directly trigger the event that HomePage listens for from AppBar
    wrapper.vm.handleLoginClick();
    await wrapper.vm.$nextTick();

    expect(pushSpy).toHaveBeenCalledWith('/login');
  });
});
