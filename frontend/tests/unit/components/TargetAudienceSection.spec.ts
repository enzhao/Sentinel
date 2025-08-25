import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import TargetAudienceSection from '@/components/TargetAudienceSection.vue';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const vuetify = createVuetify({
  components,
  directives,
});

describe('TargetAudienceSection.vue', () => {
  const goodFit = {
    title: '✅ Yes, if you are a...',
    items: ['Rule-based investor', 'Long-term thinker'],
  };
  const badFit = {
    title: '❌ Probably Not, if you are a...',
    items: ['Day Trader', 'High-frequency trader'],
  };

  it('renders title and good/bad fit lists correctly', () => {
    const title = 'Is Sentinel Right For You?';
    const wrapper = mount(TargetAudienceSection, {
      global: {
        plugins: [vuetify],
      },
      props: {
        title,
        goodFit,
        badFit,
      },
    });

    expect(wrapper.find('h2').text()).toBe(title);

    // Check good fit section
    expect(wrapper.find('.text-success').text()).toBe(goodFit.title);
    const goodFitItems = wrapper.findAll('.text-success + .v-list .v-list-item-title');
    expect(goodFitItems.length).toBe(goodFit.items.length);
    goodFitItems.forEach((item, index) => {
      expect(item.text()).toBe(goodFit.items[index]);
    });

    // Check bad fit section
    expect(wrapper.find('.text-error').text()).toBe(badFit.title);
    const badFitItems = wrapper.findAll('.text-error + .v-list .v-list-item-title');
    expect(badFitItems.length).toBe(badFit.items.length);
    badFitItems.forEach((item, index) => {
      expect(item.text()).toBe(badFit.items[index]);
    });
  });

  it('renders with empty goodFit and badFit items', () => {
    const title = 'Is Sentinel Right For You?';
    const emptyGoodFit = { title: 'Good', items: [] };
    const emptyBadFit = { title: 'Bad', items: [] };

    const wrapper = mount(TargetAudienceSection, {
      global: {
        plugins: [vuetify],
      },
      props: {
        title,
        goodFit: emptyGoodFit,
        badFit: emptyBadFit,
      },
    });

    expect(wrapper.find('h2').text()).toBe(title);
    expect(wrapper.findAll('.v-list-item').length).toBe(0);
  });
});
