import { defineStore } from 'pinia';
import { ref } from 'vue';

// Reference: product_spec.md Chapter 8

export const useUserStore = defineStore('user', () => {
  const displayName = ref<string | null>(null);
  const email = ref<string | null>(null);
  const defaultPortfolioId = ref<string | null>(null);

  function setUser(name: string, userEmail: string, portfolioId: string | null) {
    // Reference: product_spec.md Chapter 8
    // This action sets the user's display name, email, and default portfolio ID.
    displayName.value = name;
    email.value = userEmail;
    defaultPortfolioId.value = portfolioId;
  }

  function clearUser() {
    // Reference: product_spec.md Chapter 8
    // This action clears all user-related data from the store, typically on logout.
    displayName.value = null;
    email.value = null;
    defaultPortfolioId.value = null;
  }

  return { displayName, email, defaultPortfolioId, setUser, clearUser };
});
