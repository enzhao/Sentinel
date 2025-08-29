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
      @USER_CLICKS_HOME="handleHomeClick"
      @USER_CLICKS_DOCS="handleDocsClick"
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

const handleHomeClick = () => {
  router.push({ name: 'home' });
};

const handleDocsClick = () => {
  // As per product_spec.md, this should link to the user documentation.
  // Opening in a new tab is the standard for external/supplementary docs.
  // The final URL is /user_docs/ based on the CI build step.
  window.open('/user_docs/index.html', '_blank');
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
    actions: [], // Initialize with an empty array
  };

  if (route.meta.leadingAction) {
    props.leadingAction = route.meta.leadingAction;
  }

  // Common actions for all users, visible on wider screens.
  // Ref: product_spec.md Section 1.5
  props.actions.push({ id: 'home-link', label: 'Home', event: 'USER_CLICKS_HOME' });
  props.actions.push({ id: 'docs-link', label: 'Docs', event: 'USER_CLICKS_DOCS' });

  if (authStore.isAuthenticated) {
    // Add actions specific to authenticated users.
    props.actions.push({ id: 'dashboard-link', label: 'Dashboard', event: 'USER_CLICKS_DASHBOARD' });

    // Build the user menu with username and dropdown items.
    const username = userSettingsStore.userSettings?.username || 'User';
    props.userMenu = {
      username: username,
      items: [
        { id: 'settings-menu-item', label: 'Settings', event: 'USER_CLICKS_SETTINGS' },
        { id: 'logout-menu-item', label: 'Logout', event: 'USER_CLICKS_LOGOUT' },
      ],
    };
  } else {
    // Add the login action for unauthenticated users.
    props.actions.push({ id: 'login-link', label: 'Login', event: 'USER_CLICKS_LOGIN' });
  }

  return props;
});
</script>

<style scoped>
/* Add any specific styles for the layout here */
</style>