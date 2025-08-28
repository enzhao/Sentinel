// frontend/tests/unit/components/SelectField.spec.ts
import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import SelectField from '@/components/SelectField.vue';

describe('SelectField.vue', () => {
  const items = [
    { id: '1', name: 'Option 1' },
    { id: '2', name: 'Option 2' },
  ];

  const mountComponent = (props: any) => {
    return mount(SelectField, {
      props: {
        label: 'Test Label',
        items,
        itemTitle: 'name',
        itemValue: 'id',
        ...props,
      },
      // Per your observation, Vuetify is initialized globally in the test setup file.
      // We remove the local plugin registration to prevent re-registering components
      // and directives, which was causing the console warnings.
    });
  };

  it('renders the label and passes items correctly', () => {
    const wrapper = mountComponent({ modelValue: '1' }); // mountComponent provides the necessary props
    const vSelect = wrapper.findComponent({ name: 'VSelect' });

    expect(vSelect.exists()).toBe(true);
    expect(vSelect.props('label')).toBe('Test Label');
    expect(vSelect.props('items')).toEqual(items);
    expect(vSelect.props('itemTitle')).toBe('name');
    expect(vSelect.props('itemValue')).toBe('id');
  });

  it('emits update:modelValue when the selection changes', async () => {
    const wrapper = mountComponent({ modelValue: '1' }); // mountComponent provides the necessary props
    const vSelect = wrapper.findComponent({ name: 'VSelect' });

    // In an integration test with the real component, we verify the wiring
    // by simulating the event emission from the child component.
    await vSelect.vm.$emit('update:modelValue', '2');

    expect(wrapper.emitted()).toHaveProperty('update:modelValue');
    expect(wrapper.emitted()['update:modelValue'][0]).toEqual(['2']);
  });
});
