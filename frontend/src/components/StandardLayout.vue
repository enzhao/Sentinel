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
      @USER_CLICKS_DASHBOARD="handleDashboardClick"
      @USER_CLICKS_BACK="handleBackClick"
    />

    <v-main>
      <v-container fluid>
        <!-- The current view from the router will be rendered here -->
        <slot name="body"></slot>
      </v-container>
    </v-main>

    <slot name="fab"></slot>
    <!--
      The v-footer component with the `app` prop ensures that the footer content
      is always visible and correctly positioned at the bottom of the viewport.
    -->
    <v-footer app><slot name="footer"></slot></v-footer>
  </v-app>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useUserSettingsStore } from '@/stores/userSettings';
import AppBar from '@/components/AppBar.vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const userSettingsStore = useUserSettingsStore();

// Watch for authentication changes to fetch user settings when the user logs in.
// This logic lives in the layout because the layout is the component that
// directly depends on the user settings for its display. The `immediate: true`
// option is the key to fixing the page reload issue, as it ensures the
// watcher runs on component mount with the current auth state.
watch(
  () => authStore.isAuthenticated,
  (isAuth) => {
    if (isAuth && !userSettingsStore.userSettings) {
      userSettingsStore.fetchUserSettings();
    }
  },
  { immediate: true }
);
// --- Global Event Handlers ---
// These handlers are triggered by events from the central AppBar.
// This aligns with product_spec.md (1.6.3) for a central app shell.

const handleLoginClick = () => {
  router.push({ name: 'login' });
};

const handleLogout = async () => {
  try {
    const success = await authStore.logout();
    if (success) {
      userSettingsStore.clearUserSettings();
      // On successful logout, navigate to the home page.
      router.push({ name: 'home' });
    }
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

const handleSettingsClick = () => {
  router.push({ name: 'settings' });
};

const handleDashboardClick = () => {
  router.push({ name: 'dashboard' });
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
  // Diagnostic logging to help debug reactivity issues.
  console.log('DIAGNOSTIC: Re-computing appBarProps...');
  console.log(`  - authStore.isAuthenticated: ${authStore.isAuthenticated}`);
  console.log(`  - userSettingsStore.userSettings is present: ${!!userSettingsStore.userSettings}`);
  


  if (route.meta.leadingAction) {
    props.leadingAction = route.meta.leadingAction;
  }

  if (authStore.isAuthenticated) {
    console.log('DIAGNOSTIC: User is authenticated, building userMenu.');
    // Use a local variable for the username to handle the case where settings are still loading.
    const username = userSettingsStore.userSettings?.username || 'User';
    props.userMenu = {
      username: username,
      items: [
        { id: 'settings-menu-item', label: 'Settings', event: 'USER_CLICKS_SETTINGS' },
        { id: 'logout-menu-item', label: 'Logout', event: 'USER_CLICKS_LOGOUT' },
      ],
    };
    // Add a dashboard link if the user is authenticated and not already on the dashboard
    if (route.name !== 'dashboard') {
      props.actions = [{ id: 'dashboard-link', label: 'Dashboard', event: 'USER_CLICKS_DASHBOARD' }];
    }
  } else {
    console.log('DIAGNOSTIC: User is NOT authenticated, building login action.');
    props.actions = [{ label: 'Login', event: 'USER_CLICKS_LOGIN' }];
  }

  // Log the final object to see exactly what props are being generated.
  console.log('DIAGNOSTIC: Final appBarProps:', JSON.parse(JSON.stringify(props)));
  return props;
});
</script>

<style scoped>
/* Add any specific styles for the layout here */
</style>