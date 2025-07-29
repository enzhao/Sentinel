import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import SignUpView from '@/views/SignUpView.vue'
import { useAuthStore } from '@/stores/auth'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [{ path: '/login', name: 'login', component: { template: '<div>login</div>' } }]
const router = createRouter({ history: createWebHistory(), routes })

describe('SignUpView.vue', () => {
  it('calls signup with username and alerts on success', async () => {
    const pinia = createTestingPinia({ createSpy: vi.fn })
    const authStore = useAuthStore(pinia)
    authStore.signup = vi.fn().mockResolvedValue(undefined)
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})

    const wrapper = mount(SignUpView, {
      global: {
        plugins: [pinia, router],
      },
    })

    await wrapper.find('input[placeholder="Username"]').setValue('testuser')
    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('password123')
    await wrapper.find('form').trigger('submit.prevent')

    expect(authStore.signup).toHaveBeenCalledWith('testuser', 'test@example.com', 'password123')
    await wrapper.vm.$nextTick()
    expect(alertSpy).toHaveBeenCalledWith('Signup successful! Please log in.')

    alertSpy.mockRestore()
  })
})