import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue'
import PortfolioView from '../views/PortfolioView.vue'
import AboutView from '../views/AboutView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/portfolio',
    name: 'portfolio',
    component: PortfolioView,
    meta: { requiresAuth: true }
  }
]

export default routes
