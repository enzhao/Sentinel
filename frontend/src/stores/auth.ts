import { defineStore } from 'pinia'
import { ref } from 'vue'
import { auth } from '@/firebase'
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  type User
} from 'firebase/auth'
import router from '@/router'

let unsubscribe: () => void;

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const loading = ref(true)

  const init = () => {
    return new Promise<void>((resolve) => {
      if (unsubscribe) unsubscribe();
      
      unsubscribe = onAuthStateChanged(auth, (currentUser) => {
        user.value = currentUser
        loading.value = false
        resolve()
      })
    })
  }

  const initializeBackendUser = async () => {
    if (!auth.currentUser) {
      console.error("User not authenticated. Cannot initialize backend user.");
      return;
    }
    try {
      const token = await auth.currentUser.getIdToken();
      const response = await fetch('/api/users/initialize', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Backend initialization failed.");
      }

      console.log("Backend user initialized successfully.");
      const data = await response.json();
      // Optionally, you can use the returned portfolio data to update another store
    } catch (error) {
      console.error("Error initializing backend user:", error);
      // Decide how to handle this error. Maybe show a notification to the user.
    }
  }

  const signup = async (email: string, password: string) => {
    try {
      await createUserWithEmailAndPassword(auth, email, password)
      await initializeBackendUser();
      router.push('/') // Redirect to home after signup
    } catch (error: any) {
      alert(`Error signing up: ${error.message}`)
    }
  }

  const login = async (email: string, password: string) => {
    try {
      await signInWithEmailAndPassword(auth, email, password)
      router.push('/') // Redirect to home after login
    } catch (error: any) {
      alert(`Error logging in: ${error.message}`)
    }
  }

  const logout = async () => {
    try {
        await signOut(auth)
        // We MUST manually redirect to the login page after a successful logout.
        router.push('/login') 
    } catch (error: any) {
        alert(`Error logging out: ${error.message}`)
    }
}

  return { user, loading, init, signup, login, logout, initializeBackendUser }
})
