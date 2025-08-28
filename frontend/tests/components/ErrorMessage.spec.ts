// frontend/tests/unit/components/ErrorMessage.spec.ts
import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import ErrorMessage from '@/components/ErrorMessage.vue';

// Stub Vuetify component
const VAlert = {
  name: 'VAlert',
  template: '<div><slot /></div>',
  props: ['type', 'title', 'text', 'variant'],
};

describe('ErrorMessage.vue', () => {
  it('renders the message when the message prop is provided', () => {
    const message = 'Something went wrong.';
    const wrapper = mount(ErrorMessage, {
      props: { message },
      global: {
        stubs: { VAlert },
      },
    });

    expect(wrapper.findComponent(VAlert).exists()).toBe(true);
    expect(wrapper.text()).toContain(message);
  });

  it('does not render when the message prop is null or empty', async () => {
    const wrapper = mount(ErrorMessage, { props: { message: null }, global: { stubs: { VAlert } } });
    expect(wrapper.findComponent(VAlert).exists()).toBe(false);

    await wrapper.setProps({ message: '' });
    expect(wrapper.findComponent(VAlert).exists()).toBe(false);
  });
});
