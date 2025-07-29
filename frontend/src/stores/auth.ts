import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { auth } from '@/firebase'
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  type User as FirebaseUser
} from 'firebase/auth'
import router from '@/router'

// This function will be responsible for calling the backend to initialize the user.
const initializeBackendUser = async (username: string) => {
  if (!auth.currentUser) {
    throw new Error("User not authenticated in Firebase. Cannot initialize backend user.");
  }
  try {
    const token = await auth.currentUser.getIdToken();
    const response = await fetch('/api/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        'Idempotency-Key': crypto.randomUUID()
      },
      body: JSON.stringify({ username })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Backend user initialization failed.");
    }

    console.log("Backend user initialized successfully.");
    return await response.json();
  } catch (error) {
    console.error("Error initializing backend user:", error);
    throw error; // Re-throw the error to be caught by the signup function
  }
};


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

  const signup = async (username: string, email: string, password: string) => {
    try {
      // 1. Create the user in Firebase Auth
      await createUserWithEmailAndPassword(auth, email, password)
      
      // 2. Initialize the user in our backend
      await initializeBackendUser(username);

      // 3. Sign out the user locally after signup, so they are forced to login
      await signOut(auth);
      
      // 4. Redirect to the login page with a success message
      router.push('/login');

    } catch (error: any) {
      // TODO: Better error handling for the UI
      console.error(`Error signing up: ${error.message}`);
      throw new Error(`Error signing up: ${error.message}`);
    }
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

  return { user, loading, isAuthenticated, init, signup, login, logout }
})