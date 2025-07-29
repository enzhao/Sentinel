import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import SignUpView from '@/views/SignUpView.vue'
import { useAuthStore } from '@/stores/auth'
import { createRouter, createWebHistory } from 'vue-router'
import routes from '@/router/routes'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Use the actual app routes
const router = createRouter({ history: createWebHistory(), routes })

// Create a Vuetify instance
const vuetify = createVuetify({
  components,
  directives,
})

describe('SignUpView.vue', () => {
  it('calls the signup action with the correct credentials on form submission', async () => {
    const pinia = createTestingPinia({ createSpy: vi.fn })
    const authStore = useAuthStore(pinia)
    // Mock the signup action to resolve successfully
    authStore.signup = vi.fn().mockResolvedValue(undefined)
    
    const wrapper = mount(SignUpView, {
      global: {
        plugins: [pinia, router, vuetify],
      },
    })

    // Find the input elements within the Vuetify components and set their values
    await wrapper.find('input[type="text"]').setValue('testuser') // Username
    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('password123')
    
    // Trigger the form submission
    await wrapper.find('form').trigger('submit.prevent')

    // Assert that the signup action was called with the correct arguments
    expect(authStore.signup).toHaveBeenCalledTimes(1)
    expect(authStore.signup).toHaveBeenCalledWith('testuser', 'test@example.com', 'password123')
  })

  it('displays an error message if signup fails', async () => {
    const pinia = createTestingPinia({ createSpy: vi.fn })
    const authStore = useAuthStore(pinia)
    const errorMessage = 'Email is already in use.'
    // Mock the signup action to reject with an error
    authStore.signup = vi.fn().mockRejectedValue(new Error(errorMessage))

    const wrapper = mount(SignUpView, {
      global: {
        plugins: [pinia, router, vuetify],
      },
    })

    await wrapper.find('input[type="text"]').setValue('testuser')
    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('password123')
    await wrapper.find('form').trigger('submit.prevent')

    // Wait for the DOM to update
    await wrapper.vm.$nextTick()

    // Assert that the error message is displayed in a v-alert component
    const alert = wrapper.findComponent({ name: 'VAlert' })
    expect(alert.exists()).toBe(true)
    expect(alert.text()).toContain(errorMessage)
  })
})
