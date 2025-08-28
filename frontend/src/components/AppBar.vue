<template>
  <v-app-bar app>
    <v-app-bar-nav-icon v-if="leadingAction" @click="emit(leadingAction.event)">
      <v-icon>{{ leadingAction.icon }}</v-icon>
    </v-app-bar-nav-icon>
    <v-app-bar-title>{{ title }}</v-app-bar-title>
    <v-spacer></v-spacer>
    <!-- Simple action buttons, e.g., Login, Dashboard -->
    <v-btn v-for="action in actions" :id="action.id" :key="action.label" text @click="emit(action.event)">
      {{ action.label }}
    </v-btn>

    <!-- User menu dropdown for authenticated users -->
    <v-menu v-if="userMenu" offset-y>
      <template v-slot:activator="{ props }">
        <v-btn id="user-menu-button" icon v-bind="props">
          <v-avatar color="primary" size="36">
            <span>{{ userMenu.username.charAt(0).toUpperCase() }}</span>
          </v-avatar>
        </v-btn>
      </template>
      <v-list>
        <v-list-item v-for="(item, index) in userMenu.items" :key="index" :id="item.id" @click="emit(item.event)">
          <v-list-item-title>{{ item.label }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <!-- Alert icon with badge -->
    <v-btn v-if="alertAction" icon @click="emit(alertAction.event)">
      <v-badge v-if="alertAction.bindings.badgeVisible" color="red" dot overlap>
        <v-icon>{{ alertAction.icon }}</v-icon>
      </v-badge>
      <v-icon v-else>{{ alertAction.icon }}</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

interface Action {
  id?: string;
  label?: string;
  icon?: string;
  event: string;
}

interface AlertAction extends Action {
  bindings: {
    badgeVisible: boolean;
  };
}

interface UserMenu {
  username: string;
  items: Action[];
}

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  leadingAction: {
    type: Object as () => Action,
    default: null,
  },
  actions: {
    type: Array as () => Action[],
    default: () => [],
  },
  alertAction: {
    type: Object as () => AlertAction,
    default: null,
  },
  userMenu: {
    type: Object as () => UserMenu,
    default: null,
  },
});

const emit = defineEmits<{(event: string): void;}>();
</script>

<style scoped>
/* Add any specific styles for the app bar here */
</style>