import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import AppBar from '@/components/AppBar.vue';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const vuetify = createVuetify({
  components,
  directives,
});

describe('AppBar.vue', () => {
  const mountAppBar = (props: any) => mount(AppBar, {
    global: {
      plugins: [vuetify],
      stubs: {
        VAppBar: { template: '<header><slot name="prepend" /><slot /><slot name="append" /></header>' },
        VAppBarNavIcon: { template: '<button class="v-app-bar-nav-icon"><slot /></button>' },
        VAppBarTitle: { template: '<div class="v-app-bar-title"><slot /></div>' },
        VSpacer: { template: '<div class="v-spacer"></div>' },
        VBtn: { template: '<button class="v-btn"><slot /></button>' },
        VBadge: { template: '<span class="v-badge"><slot /></span>' },
        VIcon: { template: '<i class="v-icon"><slot /></i>' },
      },
    },
    props,
  });

  it('renders title correctly', () => {
    const wrapper = mountAppBar({
      title: 'Test Title',
    });
    expect(wrapper.find('.v-app-bar-title').text()).toBe('Test Title');
  });

  it('renders leading action icon and emits event', async () => {
    const wrapper = mountAppBar({
      title: 'Test Title',
      leadingAction: {
        icon: 'menu',
        event: 'USER_CLICKS_MENU',
      },
    });

    expect(wrapper.find('.v-app-bar-nav-icon').exists()).toBe(true);
    expect(wrapper.find('.v-app-bar-nav-icon .v-icon').text()).toBe('menu');

    await wrapper.find('.v-app-bar-nav-icon').trigger('click');
    expect(wrapper.emitted().USER_CLICKS_MENU).toBeTruthy();
  });

  it('renders multiple actions and emits events', async () => {
    const wrapper = mountAppBar({
      title: 'Test Title',
      actions: [
        {
          label: 'Login',
          event: 'USER_CLICKS_LOGIN',
        },
        {
          label: 'Register',
          event: 'USER_CLICKS_REGISTER',
        },
      ],
    });

    const buttons = wrapper.findAll('.v-btn');
    expect(buttons.length).toBe(2);
    expect(buttons[0].text()).toBe('Login');
    expect(buttons[1].text()).toBe('Register');

    await buttons[0].trigger('click');
    expect(wrapper.emitted().USER_CLICKS_LOGIN).toBeTruthy();

    await buttons[1].trigger('click');
    expect(wrapper.emitted().USER_CLICKS_REGISTER).toBeTruthy();
  });

  it('renders alert action with badge when badgeVisible is true', () => {
    const wrapper = mountAppBar({
      title: 'Test Title',
      alertAction: {
        icon: 'notifications',
        event: 'USER_CLICKS_ALERTS_ICON',
        bindings: {
          badgeVisible: true,
        },
      },
    });

    expect(wrapper.find('.v-badge').exists()).toBe(true);
    expect(wrapper.find('.v-badge .v-icon').text()).toBe('notifications');
  });

  it('renders alert action without badge when badgeVisible is false', () => {
    const wrapper = mountAppBar({
      title: 'Test Title',
      alertAction: {
        icon: 'notifications',
        event: 'USER_CLICKS_ALERTS_ICON',
        bindings: {
          badgeVisible: false,
        },
      },
    });

    expect(wrapper.find('.v-badge').exists()).toBe(false);
    expect(wrapper.find('.v-icon').text()).toBe('notifications');
  });

  it('emits alert action event when clicked', async () => {
    const wrapper = mountAppBar({
      title: 'Test Title',
      alertAction: {
        icon: 'notifications',
        event: 'USER_CLICKS_ALERTS_ICON',
        bindings: {
          badgeVisible: false,
        },
      },
    });

    await wrapper.find('.v-btn').trigger('click');
    expect(wrapper.emitted().USER_CLICKS_ALERTS_ICON).toBeTruthy();
  });
});