import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import AppBar from '@/components/AppBar.vue'
import { useAuthStore } from '@/stores/auth'
import { createRouter, createWebHistory } from 'vue-router'
import routes from '@/router/routes'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Setup
const router = createRouter({ history: createWebHistory(), routes })
const vuetify = createVuetify({ components, directives })

describe('AppBar.vue', () => {
  it('displays login and signup buttons when user is not authenticated', () => {
    const pinia = createTestingPinia({ createSpy: vi.fn })
    const authStore = useAuthStore(pinia)
    authStore.isAuthenticated = false

    const wrapper = mount({
      template: '<v-app><AppBar /></v-app>',
    }, {
      global: {
        components: {
          AppBar,
        },
        plugins: [pinia, router, vuetify],
      },
    })

    // Use `findComponent` for Vuetify components
    const loginBtn = wrapper.findAllComponents({ name: 'VBtn' }).find(btn => btn.text() === 'Log In')
    const signupBtn = wrapper.findAllComponents({ name: 'VBtn' }).find(btn => btn.text() === 'Sign Up')
    const logoutBtn = wrapper.findAllComponents({ name: 'VBtn' }).find(btn => btn.text() === 'Log Out')

    expect(loginBtn?.exists()).toBe(true)
    expect(signupBtn?.exists()).toBe(true)
    expect(logoutBtn).toBe(undefined)
  })

  it('displays user email and logout button when user is authenticated', () => {
    const pinia = createTestingPinia({ createSpy: vi.fn })
    const authStore = useAuthStore(pinia)
    authStore.isAuthenticated = true
    authStore.user = { email: 'test@example.com' } as any

    const wrapper = mount({
      template: '<v-app><AppBar /></v-app>',
    }, {
      global: {
        components: {
          AppBar,
        },
        plugins: [pinia, router, vuetify],
      },
    })

    const logoutBtn = wrapper.findAllComponents({ name: 'VBtn' }).find(btn => btn.text() === 'Log Out')
    const loginBtn = wrapper.findAllComponents({ name: 'VBtn' }).find(btn => btn.text() === 'Log In')

    expect(wrapper.text()).toContain('test@example.com')
    expect(logoutBtn?.exists()).toBe(true)
    expect(loginBtn).toBe(undefined)
  })

  it('calls the logout action when the logout button is clicked', async () => {
    const pinia = createTestingPinia({ createSpy: vi.fn })
    const authStore = useAuthStore(pinia)
    authStore.isAuthenticated = true
    authStore.user = { email: 'test@example.com' } as any
    // Mock the logout action
    authStore.logout = vi.fn()

    const wrapper = mount({
      template: '<v-app><AppBar /></v-app>',
    }, {
      global: {
        components: {
          AppBar,
        },
        plugins: [pinia, router, vuetify],
      },
    })

    const logoutBtn = wrapper.findAllComponents({ name: 'VBtn' }).find(btn => btn.text() === 'Log Out')
    await logoutBtn?.trigger('click')

    expect(authStore.logout).toHaveBeenCalledTimes(1)
  })
})
