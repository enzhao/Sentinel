import { createRouter as createVueRouter, createWebHistory, type Router } from 'vue-router'
import routes from './routes'
import { useAuthStore } from '@/stores/auth'

// Exporting a function to create a new router instance.
// This is useful for testing to ensure tests are isolated.
export const createSentinelRouter = (): Router => {
  const router = createVueRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
  })

  router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()
    // Ensure the auth state is initialized before any navigation logic.
    if (authStore.loading) {
      await authStore.init()
    }

    const isAuthenticated = authStore.isAuthenticated

    // 1. If the route requires authentication and the user is not logged in,
    //    redirect them to the login page.
    if (to.meta.requiresAuth && !isAuthenticated) {
      return next({ name: 'login' })
    }

    // 2. If the user is logged in, prevent them from accessing the home, login,
    //    or signup pages, and redirect them to their portfolio.
    if (isAuthenticated && ['home', 'login', 'signup'].includes(to.name as string)) {
      return next({ name: 'portfolio' })
    }

    // 3. Otherwise, allow the navigation to proceed.
    next()
  })

  return router
}

// Create a singleton instance for the app
const router = createSentinelRouter()

export default router

