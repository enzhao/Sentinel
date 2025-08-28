// frontend/tests/unit/components/FormSection.spec.ts
import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import FormSection from '@/components/FormSection.vue';

describe('FormSection.vue', () => {
  it('renders the title prop correctly', () => {
    const title = 'My Test Section';
    const wrapper = mount(FormSection, {
      props: { title },
    });

    // In Vuetify 3, v-card-title renders a div, not an h6.
    // The test is updated to find the correct element.
    const titleElement = wrapper.find('.v-card-title');
    expect(titleElement.exists()).toBe(true);
    expect(titleElement.text()).toBe(title);
  });

  it('renders content passed into the default slot', () => {
    const slotContent = '<div class="slot-content">Hello World</div>';
    const wrapper = mount(FormSection, {
      props: { title: 'Test' },
      slots: {
        default: slotContent,
      },
    });

    const slotElement = wrapper.find('.slot-content');
    expect(slotElement.exists()).toBe(true);
    expect(slotElement.text()).toBe('Hello World');
  });
});
