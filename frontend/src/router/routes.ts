import HomePage from '../views/HomePage.vue';
import LoginForm from '../views/LoginForm.vue';
import DashboardView from '../views/DashboardView.vue';
import UserSettingsView from '../views/UserSettingsView.vue';
import type { RouteRecordRaw } from 'vue-router';

const routes: readonly RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
    meta: {
      requiresAuth: false, // Public homepage does not require authentication
      title: 'Sentinel Home' // Ref: docs/specs/views_spec.yaml -> VIEW_HOME_PAGE
    }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginForm,
    meta: {
      requiresAuth: false, // Login page does not require authentication
      title: 'Login' // Ref: docs/specs/views_spec.yaml -> VIEW_LOGIN_FORM
    }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: {
      requiresAuth: true, // Dashboard requires authentication
      title: 'My Portfolios' // Ref: docs/specs/views_spec.yaml -> VIEW_DASHBOARD
    }
  },
  {
    path: '/settings',
    name: 'settings',
    component: UserSettingsView,
    meta: {
      requiresAuth: true, // User settings require authentication
      title: 'Settings', // Ref: docs/specs/views_spec.yaml -> VIEW_USER_SETTINGS
      // This adds the back button to the AppBar, handled by StandardLayout
      leadingAction: { icon: 'arrow_back', event: 'USER_CLICKS_BACK' }
    }
  },
  // New Portfolio Routes
  {
    path: '/portfolios/create',
    name: 'portfolio-create',
    component: () => import('@/views/PortfolioFormView.vue'),
    meta: { requiresAuth: true, viewId: 'VIEW_PORTFOLIO_FORM', title: 'Create Portfolio' }
  },
  {
    path: '/portfolios/:id',
    name: 'portfolio-detail',
    component: () => import('@/views/PortfolioDetailsView.vue'),
    meta: { requiresAuth: true, viewId: 'VIEW_PORTFOLIO_DETAIL', title: 'Portfolio Details' }
  },
  {
    path: '/portfolios/:id/edit',
    name: 'portfolio-edit',
    component: () => import('@/views/PortfolioFormView.vue'),
    meta: { requiresAuth: true, viewId: 'VIEW_PORTFOLIO_FORM', title: 'Edit Portfolio' }
  },
];

export default routes;