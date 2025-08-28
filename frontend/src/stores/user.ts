import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import { useAuthStore } from './auth';

// Reference: product_spec.md Chapter 8

export const useUserStore = defineStore('user', () => {
  const displayName = ref<string | null>(null);
  const email = ref<string | null>(null);
  const defaultPortfolioId = ref<string | null>(null);
  const authStore = useAuthStore();

  const setUser = (name: string, userEmail: string, portfolioId: string | null) => {
    // Reference: product_spec.md Chapter 8
    // This action sets the user's display name, email, and default portfolio ID.
    displayName.value = name;
    email.value = userEmail;
    defaultPortfolioId.value = portfolioId;
  };

  const clearUser = () => {
    // Reference: product_spec.md Chapter 8
    // This action clears all user-related data from the store, typically on logout.
    displayName.value = null;
    email.value = null;
    defaultPortfolioId.value = null;
  };

  // Watch for changes in the auth store's user object
  watch(() => authStore.user, (firebaseUser) => {
    if (firebaseUser) {
      setUser(firebaseUser.displayName || firebaseUser.email || 'User', firebaseUser.email || '', null);
    } else {
      clearUser();
    }
  }, { immediate: true });

  return { displayName, email, defaultPortfolioId, setUser, clearUser };
});
