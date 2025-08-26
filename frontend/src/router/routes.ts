import HomePage from '../views/HomePage.vue'
import LoginForm from '../views/LoginForm.vue'
import DashboardView from '../views/DashboardView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
    meta: { requiresAuth: false } // Public homepage does not require authentication
  },
  {
    path: '/login',
    name: 'login',
    component: LoginForm,
    meta: { requiresAuth: false } // Login page does not require authentication
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true } // Dashboard requires authentication
  }
]

export default routes