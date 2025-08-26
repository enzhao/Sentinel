import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import { createVuetify } from 'vuetify';
import ProblemSolutionSection from '@/components/ProblemSolutionSection.vue';

describe('ProblemSolutionSection.vue', () => {
  const items = [
    {
      title: 'The Problem: No Time to Watch',
      description:
        'You have a strategy, but work and family commitments prevent you from monitoring the market for the right entry and exit points.',
      icon: 'mdi-clock-outline',
    },
    {
      title: 'The Problem: High Management Fees',
      description:
        "Professional wealth managers are expensive and often don't align perfectly with your personal investment philosophy.",
      icon: 'mdi-cash-remove',
    },
    {
      title: 'The Solution: Your Personal Sentinel',
      description:
        "Sentinel automates your market surveillance. It's your always-on assistant, executing your strategy with precision so you can stay in control, save on fees, and invest with confidence.",
      icon: 'mdi-shield-account',
    },
  ];

  it('renders title and all items correctly', () => {
    const wrapper = mount(ProblemSolutionSection, {
      global: {
        plugins: [],
      },
      props: {
        title: 'For the Busy, Hands-On Investor',
        items,
      },
    });

    // Title
    expect(wrapper.find('h2.text-h4').text()).toBe(
      'For the Busy, Hands-On Investor'
    );

    // Cards
    const cards = wrapper.findAll('.v-card');
    expect(cards.length).toBe(items.length);

    items.forEach((item, index) => {
      const card = cards[index];
      const icon = card.find('.v-icon');

      expect(icon.exists()).toBe(true);
      expect(icon.classes()).toContain(item.icon);

      // Vuetify applies colors as classes like text-error / text-success
      if (item.title.includes('Problem')) {
        expect(icon.classes()).toContain('text-error');
      } else {
        expect(icon.classes()).toContain('text-success');
      }

      expect(card.find('h3.text-h6').text()).toBe(item.title);
      expect(card.find('p.text-medium-emphasis').text()).toBe(item.description);
    });
  });

  it('renders no cards if items is empty', () => {
    const wrapper = mount(ProblemSolutionSection, {
      global: {
        plugins: [],
      },
      props: {
        title: 'Empty Case',
        items: [],
      },
    });

    expect(wrapper.find('h2.text-h4').text()).toBe('Empty Case');
    expect(wrapper.findAll('.v-card').length).toBe(0);
  });

  it('handles invalid items gracefully', () => {
    const wrapper = mount(ProblemSolutionSection, {
      global: {
        plugins: [],
      },
      props: {
        title: 'Test Invalid Items',
        items: [
          { title: '', description: '', icon: '' }, // invalid empty item
        ],
      },
    });

    const cards = wrapper.findAll('.v-card');
    expect(cards.length).toBe(1);

    const card = cards[0];
    const icon = card.find('.v-icon');

    expect(icon.exists()).toBe(true);

    // Should only have v-icon (no mdi-* icon, no text-error/success)
    expect(icon.classes()).toContain('v-icon');
    expect(icon.classes().some(cls => cls.startsWith('mdi-'))).toBe(false);
    expect(icon.classes()).not.toContain('text-error');
    expect(icon.classes()).not.toContain('text-success');

    // Empty content for invalid item
    expect(card.find('h3.text-h6').text()).toBe('');
    expect(card.find('p.text-medium-emphasis').text()).toBe('');
  });
});
