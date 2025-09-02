import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import ConfirmationDialog from '@/components/ConfirmationDialog.vue';
import { createVuetify } from 'vuetify';

// This is a component-level test.
// Reference: docs/testing_strategy.md (Section 4.1)

const vuetify = createVuetify();

describe('ConfirmationDialog.vue', () => {
  it('renders props correctly', () => {
    const wrapper = mount(ConfirmationDialog, {
      global: { plugins: [vuetify] },
      props: {
        modelValue: true,
        title: 'Test Title',
        message: 'Test Message',
      },
    });

    expect(wrapper.text()).toContain('Test Title');
    expect(wrapper.text()).toContain('Test Message');
  });

  it('emits confirm event when confirm button is clicked', async () => {
    const wrapper = mount(ConfirmationDialog, {
      global: { plugins: [vuetify] },
      props: { modelValue: true, title: 't', message: 'm' },
    });

    await wrapper.find('button.v-btn[color="error"]').trigger('click');
    expect(wrapper.emitted()).toHaveProperty('confirm');
  });

  it('emits cancel event when cancel button is clicked', async () => {
    const wrapper = mount(ConfirmationDialog, {
      global: { plugins: [vuetify] },
      props: { modelValue: true, title: 't', message: 'm' },
    });

    // The cancel button is the first button in the actions
    await wrapper.findAll('button.v-btn')[0].trigger('click');
    expect(wrapper.emitted()).toHaveProperty('cancel');
  });

  it('shows loading state on confirm button', () => {
    const wrapper = mount(ConfirmationDialog, {
      global: { plugins: [vuetify] },
      props: {
        modelValue: true,
        title: 't',
        message: 'm',
        loading: true,
      },
    });

    const confirmButton = wrapper.find('button.v-btn[color="error"]');
    expect(confirmButton.classes()).toContain('v-btn--loading');
  });
});