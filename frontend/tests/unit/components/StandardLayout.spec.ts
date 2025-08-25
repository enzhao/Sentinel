import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import StandardLayout from '@/components/StandardLayout.vue';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const vuetify = createVuetify({
  components,
  directives,
});

describe('StandardLayout.vue', () => {
  it('renders header, body, and fab slots', () => {
    const wrapper = mount(StandardLayout, {
      global: {
        plugins: [vuetify],
      },
      slots: {
        header: '<div class="test-header">Header Content</div>',
        body: '<div class="test-body">Body Content</div>',
        fab: '<div class="test-fab">FAB Content</div>',
      },
    });

    expect(wrapper.find('.test-header').exists()).toBe(true);
    expect(wrapper.find('.test-header').text()).toBe('Header Content');
    expect(wrapper.find('.test-body').exists()).toBe(true);
    expect(wrapper.find('.test-body').text()).toBe('Body Content');
    expect(wrapper.find('.test-fab').exists()).toBe(true);
    expect(wrapper.find('.test-fab').text()).toBe('FAB Content');
  });

  it('renders without any slot content', () => {
    const wrapper = mount(StandardLayout, {
      global: {
        plugins: [vuetify],
      },
    });

    // Expect the main app and main content to still exist
    expect(wrapper.find('.v-application').exists()).toBe(true);
    expect(wrapper.find('.v-main').exists()).toBe(true);
    // Expect slot content not to be rendered if slots are empty
    expect(wrapper.html()).not.toContain('Header Content');
    expect(wrapper.html()).not.toContain('Body Content');
    expect(wrapper.html()).not.toContain('FAB Content');
  });
});
