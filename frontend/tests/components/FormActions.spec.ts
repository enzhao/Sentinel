// frontend/tests/unit/components/FormActions.spec.ts
import { mount, VueWrapper } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import FormActions from '@/components/FormActions.vue';

const mockActions = [
  { label: 'Cancel', event: 'USER_CLICKS_CANCEL', color: 'default' },
  { label: 'Save', event: 'USER_CLICKS_SAVE', color: 'primary' },
];

// Per your suggestion, I've analyzed the other passing tests in the project.
// They consistently use stubs to isolate the component under test. The previous
// failures occurred because of unexpected behavior when testing against the real
// Vuetify component in a JSDOM environment.
//
// This revised approach stubs <v-btn> and focuses on verifying that FormActions
// passes the correct props to its children. This is a more robust unit testing strategy.
const VBtnStub = {
  name: 'VBtn',
  // The button is disabled if the `loading` prop is true, mimicking real component behavior.
  template: '<button :disabled="loading"><slot /></button>',
  // We define the props the stub should expect to receive.
  props: ['color', 'loading'],
};

describe('FormActions.vue', () => {
  const mountComponent = (props = {}): VueWrapper<any> => {
    return mount(FormActions, {
      props: {
        actions: mockActions,
        ...props,
      },
      global: {
        stubs: {
          'v-btn': VBtnStub,
          'v-card-actions': { template: '<div><slot /></div>' },
        },
      },
    });
  };

  it('renders Save and Cancel buttons', () => {
    const wrapper = mountComponent();
    const buttons = wrapper.findAllComponents(VBtnStub);
    expect(buttons.length).toBe(2);

    expect(buttons[0].text()).toBe(mockActions[0].label);
    expect(buttons[1].text()).toBe(mockActions[1].label);
  });

  it('emits USER_CLICKS_SAVE when the Save button is clicked', async () => {
    const wrapper = mountComponent();
    const buttons = wrapper.findAllComponents(VBtnStub);

    const saveButton = buttons[1]; // The "Save" button is the second one.
    await saveButton.trigger('click');

    expect(wrapper.emitted()).toHaveProperty(mockActions[1].event);
  });

  it('emits USER_CLICKS_CANCEL when the Cancel button is clicked', async () => {
    const wrapper = mountComponent();
    const buttons = wrapper.findAllComponents(VBtnStub);

    const cancelButton = buttons[0]; // The "Cancel" button is the first one.
    await cancelButton.trigger('click');

    expect(wrapper.emitted()).toHaveProperty(mockActions[0].event);
  });

  it('disables buttons when the loading prop is true', () => {
    const wrapper = mountComponent({ loading: true });
    const buttons = wrapper.findAllComponents(VBtnStub);

    expect(buttons.length).toBe(mockActions.length);

    expect((buttons[0].element as HTMLButtonElement).disabled).toBe(true);
    expect((buttons[1].element as HTMLButtonElement).disabled).toBe(true);
  });
});
