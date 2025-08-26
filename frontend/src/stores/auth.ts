import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getAuth, onAuthStateChanged, signInWithEmailAndPassword, signOut } from 'firebase/auth'
import type { User as FirebaseUser } from 'firebase/auth'
import router from '@/router'
import { useUserStore } from './user'

// Reference: product_spec.md Chapter 8

export const useAuthStore = defineStore('auth', () => {
  const user = ref<FirebaseUser | null>(null)
  const isAuthenticated = computed(() => user.value !== null)
  const loading = ref(true)
  const auth = getAuth()
  const userStore = useUserStore()

  function setAuthStatus(status: boolean) {
    // Reference: product_spec.md Chapter 8
    // This action updates the authentication status in the store.
    // It is called by the onAuthStateChanged listener.
    // The router guards then react to this status.
    if (!status) {
      user.value = null;
    }
  }

  function setUser(firebaseUser: FirebaseUser | null) {
    // Reference: product_spec.md Chapter 8
    // This action sets the Firebase user object in the store.
    // It is called by the onAuthStateChanged listener.
    user.value = firebaseUser;
    if (firebaseUser) {
      userStore.setUser(firebaseUser.displayName || firebaseUser.email || 'User', firebaseUser.email || '', null)
    } else {
      userStore.clearUser()
    }
  }

  function setLoading(isLoading: boolean) {
    // Reference: product_spec.md Chapter 8
    // This action updates the loading status of the authentication state.
    // It is used to indicate when the initial authentication check is complete.
    loading.value = isLoading;
  }

  async function init() {
    // Reference: product_spec.md Chapter 8
    // This function initializes the authentication state by setting up a listener
    // for Firebase authentication changes. It ensures the app's auth state
    // is always in sync with Firebase.
    return new Promise<void>((resolve) => {
      onAuthStateChanged(auth, (firebaseUser) => {
        setUser(firebaseUser);
        setAuthStatus(!!firebaseUser);
        setLoading(false);
        resolve();
      });
    });
  }

  async function login(email: string, password: string) {
    // Reference: product_spec.md Chapter 8, docs/specs/ui_flows_spec.yaml FLOW_LOGIN
    // This function handles user login via Firebase Authentication.
    // On successful login, the onAuthStateChanged listener (set up in init())
    // will automatically update the store's user and isAuthenticated state,
    // and the router's beforeEach guard will handle redirection to the dashboard.
    try {
      await signInWithEmailAndPassword(auth, email, password)
      // The onAuthStateChanged listener will handle updating the state.
      // After it's done, we navigate to the dashboard.
      router.push({ name: 'dashboard' }) 
      return true
    } catch (error: any) {
      console.error('Login failed:', error.message)
      throw error
    }
  }

  async function logout() {
    // Reference: product_spec.md Chapter 8, docs/specs/ui_flows_spec.yaml FLOW_LOGOUT
    // This function handles user logout via Firebase Authentication.
    // On successful logout, the onAuthStateChanged listener will clear the user,
    // and the router's beforeEach guard will handle redirection to the home page.
    try {
      await signOut(auth)
      router.push({ name: 'home' }) // Explicitly navigate to home after logout
      return true
    } catch (error: any) {
      console.error('Logout failed:', error.message)
      throw error
    }
  }

  return { user, isAuthenticated, loading, init, login, logout, setAuthStatus, setUser, setLoading }
})