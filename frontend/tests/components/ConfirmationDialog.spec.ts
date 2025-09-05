import { mount, VueWrapper } from '@vue/test-utils';
import { describe, it, expect, afterEach } from 'vitest';
import ConfirmationDialog from '@/components/ConfirmationDialog.vue';
import { h } from 'vue';
import { VApp } from 'vuetify/components';

// This is a component-level test.
// Reference: docs/testing_strategy.md (Section 4.1)

describe('ConfirmationDialog.vue', () => {
  let wrapper: VueWrapper<any>;

  // Helper to mount the component correctly inside VApp.
  // v-dialog is a teleported component and needs to be mounted within a v-app
  // and attached to the document body to be visible in the JSDOM.
  const mountComponent = (props: any) => {
    wrapper = mount(VApp, {
      slots: { default: h(ConfirmationDialog, props) },
      attachTo: document.body,
    });
  };

  afterEach(() => {
    // Clean up the DOM after each test
    if (wrapper) {
      wrapper.unmount();
    }
  });

  it('renders props correctly', () => {
    mountComponent({
      modelValue: true,
      title: 'Test Title',
      message: 'Test Message',
    });

    // Because v-dialog teleports its content, we query the global document
    expect(document.body.innerHTML).toContain('Test Title');
    expect(document.body.innerHTML).toContain('Test Message');
  });

  it('emits confirm event when confirm button is clicked', async () => {
    mountComponent({ modelValue: true, title: 't', message: 'm' });
    const dialogWrapper = wrapper.findComponent(ConfirmationDialog);

    // The confirm button is the second button in the actions
    const confirmButton = document.querySelectorAll('button.v-btn')[1] as HTMLElement;
    expect(confirmButton).not.toBeNull();
    await confirmButton.click();

    expect(dialogWrapper.emitted()).toHaveProperty('confirm');
  });

  it('emits cancel event when cancel button is clicked', async () => {
    mountComponent({ modelValue: true, title: 't', message: 'm' });
    const dialogWrapper = wrapper.findComponent(ConfirmationDialog);

    // The cancel button is the first button in the actions
    const cancelButton = document.querySelectorAll('button.v-btn')[0] as HTMLElement;
    expect(cancelButton).not.toBeNull();
    await cancelButton.click();

    expect(dialogWrapper.emitted()).toHaveProperty('cancel');
  });

  it('shows loading state on confirm button', () => {
    mountComponent({ modelValue: true, title: 't', message: 'm', loading: true });

    // The confirm button is the second button in the actions
    const confirmButton = document.querySelectorAll('button.v-btn')[1];
    expect(confirmButton).not.toBeNull();
    // Vuetify adds the v-btn--loading class when the loading prop is true
    expect(confirmButton?.classList.contains('v-btn--loading')).toBe(true);
  });
});