<template>
  <v-app>
    <AppBar
      title="Sentinel"
      :actions="appBarActions"
      @USER_CLICKS_LOGIN="handleLoginClick"
      @USER_CLICKS_LOGOUT="handleLogout"
    />

    <v-main>
      <v-container fluid>
        <slot name="body"></slot>
      </v-container>
    </v-main>

    <slot name="fab"></slot>
  </v-app>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import AppBar from '@/components/AppBar.vue'; // Import the AppBar

// --- This layout is now the "Smart" App Shell ---

// 3. Get the router and auth store instances
const router = useRouter();
const authStore = useAuthStore();

// 4. Define the handler methods for global events
const handleLoginClick = () => {
  router.push({ name: 'login' });
};

const handleLogout = async () => {
  try {
    await authStore.logout();
    // The logout action in the store will handle the redirection to 'home'
  } catch (error) {
    console.error('Logout failed:', error);
    // Optionally, you could use a global notification service here
  }
};

// 5. Create a computed property to dynamically set the AppBar actions
//    based on the user's authentication state.
const appBarActions = computed(() => {
  if (authStore.isAuthenticated) {
    return [{ label: 'Logout', event: 'USER_CLICKS_LOGOUT' }];
  } else {
    return [{ label: 'Login', event: 'USER_CLICKS_LOGIN' }];
  }
});
</script>

<style scoped>
/* Add any specific styles for the layout here */
</style>