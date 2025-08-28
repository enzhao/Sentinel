import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import { createVuetify } from 'vuetify';
import KeyFeaturesSection from '@/components/KeyFeaturesSection.vue';

describe('KeyFeaturesSection.vue', () => {
  const features = [
    {
      icon: 'mdi-strategy',
      title: 'Define Your Strategy',
      description: 'Codify your investment philosophy.',
    },
    {
      icon: 'mdi-robot',
      title: 'Automated Monitoring',
      description: 'Let Sentinel watch the market.',
    },
    {
      icon: 'mdi-shield-check',
      title: 'Stay in Control',
      description:
        'Receive timely, data-driven alerts, allowing you to execute your plan with discipline.',
    },
  ];

  it('renders all features correctly', () => {
    const wrapper = mount(KeyFeaturesSection, {
      global: {
        plugins: [],
      },
      props: {
        features,
      },
    });

    // Container exists
    expect(wrapper.find('.key-features-section').exists()).toBe(true);

    // Title exists
    expect(wrapper.find('h2.text-h4').text()).toBe('Key Features');

    // Cards exist
    const featureCards = wrapper.findAll('.v-card');
    expect(featureCards.length).toBe(features.length);

    // Check each feature
    features.forEach((feature, index) => {
      const card = featureCards[index];
      const icon = card.find('.v-icon');
      expect(icon.exists()).toBe(true);

      // Vuetify renders the full class name like mdi-xxx
      expect(icon.classes()).toContain(feature.icon);

      // Title and description
      expect(card.find('h3.text-h6').text()).toBe(feature.title);
      expect(card.find('p.text-medium-emphasis').text()).toBe(feature.description);
    });
  });

  it('renders without features', () => {
    const wrapper = mount(KeyFeaturesSection, {
      global: {
        plugins: [],
      },
      props: {
        features: [],
      },
    });

    expect(wrapper.find('.key-features-section').exists()).toBe(true);
    expect(wrapper.findAll('.v-card').length).toBe(0);
    expect(wrapper.find('h2.text-h4').text()).toBe('Key Features');
  });

  it('handles invalid feature props gracefully', () => {
    const invalidFeatures = [
      {
        icon: '', // invalid
        title: '',
        description: '',
      },
    ];

    const wrapper = mount(KeyFeaturesSection, {
      global: {
        plugins: [],
      },
      props: {
        features: invalidFeatures,
      },
    });

    const featureCards = wrapper.findAll('.v-card');
    expect(featureCards.length).toBe(1);

    const card = featureCards[0];
    const icon = card.find('.v-icon');
    expect(icon.exists()).toBe(true);

    // When icon="" Vuetify still renders <i class="v-icon"></i>
    expect(icon.classes()).toContain('v-icon');
    expect(card.find('h3.text-h6').text()).toBe('');
    expect(card.find('p.text-medium-emphasis').text()).toBe('');
  });
});
