<template>
  <v-app>
    <!--
      This is the single, centralized AppBar for the entire application,
      acting as the "Application Shell" described in product_spec.md (1.6.3).
      Its properties are dynamically computed based on the current route and
      authentication state.
    -->
    <AppBar
      v-bind="appBarProps"
      @USER_CLICKS_LOGIN="handleLoginClick"
      @USER_CLICKS_LOGOUT="handleLogout"
      @USER_CLICKS_SETTINGS="handleSettingsClick"
      @USER_CLICKS_BACK="handleBackClick"
    />

    <v-main>
      <v-container fluid>
        <!-- The current view from the router will be rendered here -->
        <slot name="body"></slot>
      </v-container>
    </v-main>

    <slot name="fab"></slot>
    <!-- Slot for footer content, as specified in views_spec.yaml -->
    <slot name="footer"></slot>
  </v-app>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useUserSettingsStore } from '@/stores/userSettings';
import AppBar from '@/components/AppBar.vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const userSettingsStore = useUserSettingsStore();

// --- Global Event Handlers ---
// These handlers are triggered by events from the central AppBar.
// This aligns with product_spec.md (1.6.3) for a central app shell.

const handleLoginClick = () => {
  router.push({ name: 'login' });
};

const handleLogout = async () => {
  try {
    await authStore.logout();
    // The authStore's logout action handles redirection.
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

const handleSettingsClick = () => {
  router.push({ name: 'settings' });
};

const handleBackClick = () => {
  router.back();
};

// --- Dynamic AppBar Properties ---
// This computed property dynamically builds the props for the AppBar
// based on the user's auth state and the current route's metadata.
const appBarProps = computed(() => {
  const props: any = {
    title: route.meta.title || 'Sentinel',
  };

  if (route.meta.leadingAction) {
    props.leadingAction = route.meta.leadingAction;
  }

  if (authStore.isAuthenticated) {
    props.userMenu = {
      username: userSettingsStore.userSettings?.username || 'User',
      items: [
        { label: 'Settings', event: 'USER_CLICKS_SETTINGS' },
        { label: 'Logout', event: 'USER_CLICKS_LOGOUT' },
      ],
    };
  } else {
    props.actions = [{ label: 'Login', event: 'USER_CLICKS_LOGIN' }];
  }

  return props;
});
</script>

<style scoped>
/* Add any specific styles for the layout here */
</style>