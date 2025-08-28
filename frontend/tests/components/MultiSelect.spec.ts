// frontend/tests/unit/components/MultiSelect.spec.ts
import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import MultiSelect from '@/components/MultiSelect.vue';

describe('MultiSelect.vue', () => {
  // The component expects a simple array of strings for its options.
  const options = ['EMAIL', 'PUSH'];

  const mountComponent = (props: any) => {
    return mount(MultiSelect, {
      props: {
        label: 'Test MultiSelect',
        options, // The component prop is named 'options'
        ...props,
      },
      // We use the real Vuetify components, which are globally available
      // via the test setup file, to ensure high-fidelity testing.
    });
  };

  it('renders the label and passes items correctly with multiple prop', () => {
    const wrapper = mountComponent({ modelValue: ['EMAIL'] });
    const vSelect = wrapper.findComponent({ name: 'VSelect' });

    expect(vSelect.exists()).toBe(true);
    expect(vSelect.props('label')).toBe('Test MultiSelect');
    // The component passes its `options` prop to the `items` prop of VSelect
    expect(vSelect.props('items')).toEqual(options);
    expect(vSelect.props('multiple')).toBe(true);
    expect(vSelect.props('chips')).toBe(true);
  });

  it('emits update:modelValue when the selection changes', async () => {
    const wrapper = mountComponent({ modelValue: ['EMAIL'] });
    const vSelect = wrapper.findComponent({ name: 'VSelect' });

    // Simulate the event emission from the child VSelect component
    await vSelect.vm.$emit('update:modelValue', ['EMAIL', 'PUSH']);

    expect(wrapper.emitted()).toHaveProperty('update:modelValue');
    expect(wrapper.emitted()['update:modelValue'][0]).toEqual([['EMAIL', 'PUSH']]);
  });
});
