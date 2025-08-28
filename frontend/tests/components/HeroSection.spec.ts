import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import HeroSection from '@/components/HeroSection.vue';

describe('HeroSection.vue', () => {
  it('renders title and subtitle correctly', () => {
    const title = 'Test Title';
    const subtitle = 'Test Subtitle';
    const wrapper = mount(HeroSection, {
      global: {
        plugins: [],
      },
      props: {
        title,
        subtitle,
      },
    });

    expect(wrapper.find('h1').text()).toBe(title);
    expect(wrapper.find('p').text()).toBe(subtitle);
  });

  it('emits USER_CLICKS_GET_STARTED event when button is clicked', async () => {
    const wrapper = mount(HeroSection, {
      global: {
        plugins: [],
      },
      props: {
        title: 'Test Title',
        subtitle: 'Test Subtitle',
      },
    });

    await wrapper.find('button').trigger('click');
    expect(wrapper.emitted().USER_CLICKS_GET_STARTED).toBeTruthy();
  });
});
