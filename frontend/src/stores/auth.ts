import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { auth } from '@/firebase'
import {
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  type User as FirebaseUser
} from 'firebase/auth'
import router from '@/router'

let unsubscribe: (() => void) | null = null;

export const useAuthStore = defineStore('auth', () => {
  const user = ref<FirebaseUser | null>(null)
  const loading = ref(true)
  const isAuthenticated = computed(() => !!user.value)

  const init = () => {
    return new Promise<void>((resolve) => {
      if (unsubscribe) {
        loading.value = false;
        resolve();
        return;
      }
      
      unsubscribe = onAuthStateChanged(auth, (currentUser) => {
        user.value = currentUser
        loading.value = false
        resolve()
      })
    })
  }

  const login = async (email: string, password: string) => {
    try {
      await signInWithEmailAndPassword(auth, email, password)
      router.push('/portfolio')
    } catch (error: any)      {
      console.error(`Login failed: ${error.message}`);
      throw new Error(`Login failed: ${error.message}`);
    }
  }

  const logout = async () => {
    try {
        await signOut(auth)
        user.value = null
        router.push('/') 
    } catch (error: any) {
        console.error(`Error logging out: ${error.message}`);
        alert(`Error logging out: ${error.message}`)
    }
}

  return { user, loading, isAuthenticated, init, login, logout }
})