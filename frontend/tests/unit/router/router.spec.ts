import { describe, it, expect, beforeEach, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { createSentinelRouter } from '@/router'
import { useAuthStore } from '@/stores/auth'
import type { Router } from 'vue-router'

vi.mock('@/stores/auth', () => ({
  useAuthStore: vi.fn(() => ({
    isAuthenticated: false,
    loading: false,
    init: vi.fn().mockResolvedValue(undefined),
  })),
}))

describe('Router', () => {
  let router: Router

  beforeEach(() => {
    setActivePinia(createPinia())
    // Reset mocks before each test
    vi.clearAllMocks()
  })

  it('redirects to portfolio if logged in and trying to access home', async () => {
    vi.mocked(useAuthStore).mockReturnValue({
      isAuthenticated: true,
      loading: false,
      init: vi.fn().mockResolvedValue(undefined),
    } as any)
    router = createSentinelRouter()
    
    router.push('/')
    await router.isReady()

    expect(router.currentRoute.value.name).toBe('portfolio')
  })

  it('redirects to login if not logged in and trying to access a protected route', async () => {
    vi.mocked(useAuthStore).mockReturnValue({
      isAuthenticated: false,
      loading: false,
      init: vi.fn().mockResolvedValue(undefined),
    } as any)
    router = createSentinelRouter()

    router.push('/portfolio')
    await router.isReady()

    expect(router.currentRoute.value.name).toBe('login')
  })

  it('redirects to portfolio if logged in and trying to access login', async () => {
    vi.mocked(useAuthStore).mockReturnValue({
      isAuthenticated: true,
      loading: false,
      init: vi.fn().mockResolvedValue(undefined),
    } as any)
    router = createSentinelRouter()

    router.push('/login')
    await router.isReady()

    expect(router.currentRoute.value.name).toBe('portfolio')
  })
})
